#
# Copyright (c) 2021, 2022 Astroncia
# Copyright (c) 2023-2025 liya <liyaliya@tutamail.com>
#
# This file is part of yuki-iptv.
#
# yuki-iptv is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# yuki-iptv is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with yuki-iptv. If not, see <https://www.gnu.org/licenses/>.
#
# The Font Awesome pictograms are licensed under the CC BY 4.0 License.
# Font Awesome Free 5.15.4 by @fontawesome - https://fontawesome.com
# https://creativecommons.org/licenses/by/4.0/
#
import functools
import logging
import subprocess
from urllib.parse import urlparse
from PyQt6 import QtCore
from yuki_iptv.i18n import _
from yuki_iptv.settings import parse_settings

logger = logging.getLogger(__name__)

# Time to wait for ffmpeg to finish gracefully after sending "q" (ms)
GRACEFUL_STOP_TIMEOUT = 5000

# ffmpeg exit code for AVERROR_OPTION_NOT_FOUND ("Option ... not found.")
FFMPEG_EXIT_OPTION_NOT_FOUND = 8


class YukiData:
    ffmpeg_proc = None
    ffmpeg_processes = None
    show_record_exception = None


def is_hls_url(url):
    """Cheap heuristic: does this URL look like an HLS playlist?"""
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    return ".m3u8" in parsed.path.lower() or ".m3u8" in parsed.query.lower()


@functools.lru_cache(maxsize=1)
def ffmpeg_supports_extension_picky():
    """
    -extension_picky is a private option of the hls demuxer, so it is only
    valid if the installed ffmpeg knows it. Probe once and cache the result.
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-h", "demuxer=hls"],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return "extension_picky" in (result.stdout + result.stderr)
    except Exception:
        logger.warning("Could not probe ffmpeg for extension_picky support")
        return False


def strip_extension_picky(args):
    args = list(args)
    if "-extension_picky" in args:
        i = args.index("-extension_picky")
        del args[i : i + 2]
    return args


def is_ffmpeg_recording():
    ret = -2
    if YukiData.ffmpeg_proc:
        if YukiData.ffmpeg_proc.processId() == 0:
            YukiData.ffmpeg_proc = None
            ret = True
        else:
            ret = False
    return ret


def _tail(data):
    try:
        return "\n".join(
            bytes(data).decode("utf-8", errors="replace").split("\n")[-15:]
        )
    except Exception:
        return str(data)


def exit_handler(process, exit_code, _exit_status):
    is_killed = False
    try:
        is_killed = process._yuki_killed
    except Exception:
        pass
    if is_killed:
        return
    standard_output = process.readAllStandardOutput()
    standard_error = process.readAllStandardError()

    # -extension_picky only exists on the hls demuxer. If the heuristic was
    # wrong and ffmpeg rejected it, retry once without it, on the same
    # QProcess object so callers holding a reference keep a valid handle.
    retry_arr = getattr(process, "_yuki_retry_arr", None)
    if (
        retry_arr
        and exit_code == FFMPEG_EXIT_OPTION_NOT_FOUND
        and b"extension_picky" in bytes(standard_error)
    ):
        logger.warning("ffmpeg rejected -extension_picky, retrying without it")
        process._yuki_retry_arr = None
        process.start("ffmpeg", retry_arr)
        return

    crashed = _exit_status != QtCore.QProcess.ExitStatus.NormalExit
    if not crashed and exit_code == 0:
        logger.info("ffmpeg finished")
        return

    # Non-zero exit without a crash: connection error, HTTP 403/404,
    # invalid URL etc. - reported too
    logger.warning(f"ffmpeg failed (exit code {exit_code}, crashed: {crashed})")
    if YukiData.show_record_exception:
        YukiData.show_record_exception(
            (_("ffmpeg crashed!") if crashed else _("Recording failed!")) + "\n"
            "" + _("exit code:") + " " + str(exit_code) + ""
            "\nstdout:\n" + _tail(standard_output) + ""
            "\nstderr:\n" + _tail(standard_error)
        )


def error_handler(error):
    if error == QtCore.QProcess.ProcessError.FailedToStart:
        # "finished" is not emitted in this case
        logger.error("ffmpeg failed to start")
        if YukiData.show_record_exception:
            YukiData.show_record_exception(
                _("ffmpeg could not be started!")
                + "\n"
                + _("Make sure ffmpeg is installed and available in PATH.")
            )


def _start_ffmpeg(arr, retry_arr=None):
    proc = QtCore.QProcess()
    proc._yuki_retry_arr = retry_arr
    proc.finished.connect(
        lambda exit_code, exit_status: exit_handler(proc, exit_code, exit_status)
    )
    proc.errorOccurred.connect(lambda error: error_handler(error))
    proc.start("ffmpeg", arr)
    return proc


def record(
    input_url,
    out_file,
    channel_name,
    http_referer,
    get_ua_ref_for_channel,
    is_return=False,
):
    settings, settings_loaded = parse_settings()
    if http_referer == "Referer: ":
        http_referer = ""
    useragent_ref, referer_ref = get_ua_ref_for_channel(channel_name)
    user_agent = useragent_ref
    origin_add = ""
    if referer_ref:
        http_referer = f"Referer: {referer_ref}"
        originURL = ""
        if referer_ref.endswith("/"):
            originURL = referer_ref[:-1]
        if originURL:
            origin_add = "Origin: " + originURL + "\r\n"
    logger.info(f"Using user agent '{user_agent}' for record channel '{channel_name}'")
    logger.info(f"HTTP headers: '{http_referer}'")
    retry_arr = None
    if input_url.startswith("http://") or input_url.startswith("https://"):
        use_picky = is_hls_url(input_url) and ffmpeg_supports_extension_picky()
        arr = [
            "-nostats",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-user_agent",
            user_agent,
            "-headers",
            http_referer + "\r\n" + origin_add,
            *(["-extension_picky", "0"] if use_picky else []),
            "-reconnect",
            "1",
            "-reconnect_streamed",
            "1",
            "-reconnect_on_network_error",
            "1",
            "-reconnect_on_http_error",
            "503",
            "-reconnect_delay_max",
            "5",
            "-i",
            input_url,
            # Select all streams first, otherwise the negative maps below
            # have no effect and only one audio track is recorded
            "-map",
            "0",
            "-map",
            "-0:s?",
            "-sn",
            "-map",
            "-0:d?",
            "-map",
            "-0:t?",
            "-codec",
            "copy",
            "-max_muxing_queue_size",
            "4096",
            out_file,
        ]
        if use_picky:
            retry_arr = strip_extension_picky(arr)
    else:
        arr = [
            "-nostats",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-i",
            input_url,
            # Select all streams first, otherwise the negative maps below
            # have no effect and only one audio track is recorded
            "-map",
            "0",
            "-map",
            "-0:s?",
            "-sn",
            "-map",
            "-0:d?",
            "-map",
            "-0:t?",
            "-codec",
            "copy",
            "-max_muxing_queue_size",
            "4096",
            out_file,
        ]
    if not is_return:
        YukiData.ffmpeg_proc = _start_ffmpeg(arr, retry_arr)
    else:
        return _start_ffmpeg(arr, retry_arr)


def terminate_record_process(proc, wait=False):
    """Stops ffmpeg gracefully so the output file is finalized.

    "q" is sent to ffmpeg's stdin first; the process is killed only if it
    does not exit in time. wait=True blocks (used on application exit,
    when timers would never fire).
    """
    proc._yuki_killed = True
    if proc.processId() == 0:
        return
    try:
        proc.write(b"q")
        proc.closeWriteChannel()
    except Exception:
        logger.exception("Failed to send 'q' to ffmpeg")

    if wait:
        if not proc.waitForFinished(GRACEFUL_STOP_TIMEOUT):
            proc.kill()
            proc.waitForFinished(GRACEFUL_STOP_TIMEOUT)
        return

    def force_stop():
        if proc.processId() != 0:
            logger.warning("ffmpeg did not exit in time, killing")
            proc.kill()

    QtCore.QTimer.singleShot(GRACEFUL_STOP_TIMEOUT, force_stop)


def stop_record(wait=False):
    if YukiData.ffmpeg_proc:
        terminate_record_process(YukiData.ffmpeg_proc, wait)


def init_record(show_exception, ffmpeg_processes):
    YukiData.show_record_exception = show_exception
    YukiData.ffmpeg_processes = ffmpeg_processes
