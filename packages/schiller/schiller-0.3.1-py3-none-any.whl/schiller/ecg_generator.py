"""ECG Generator."""
import numpy as np


def get_ecg_beat() -> np.ndarray:
    """Creates a synthetic ECG heart beat."""

    qrs_w = 150
    q_amp = 1000

    pq = 60
    p_dur = 100
    p_amp = 200

    st_dur = 20
    t_dur = 300
    t_amp = 300

    # P wave
    tot_len = p_dur + pq + qrs_w + st_dur + t_dur
    assert tot_len < 1000
    out_arr = np.zeros((1000,), dtype=np.int32)
    out_arr[:p_dur] = get_peak(p_dur, p_amp)

    # QRS
    qrs_on = p_dur + pq
    qrs_third = qrs_w // 3
    qrs_two_third = 2 * qrs_third
    qrs_base_peak = get_peak(qrs_two_third, 1)
    out_arr[qrs_on : qrs_on + qrs_two_third] = -q_amp // 4 * qrs_base_peak
    out_arr[qrs_on + qrs_third : qrs_on + 3 * qrs_third] += (
        q_amp * qrs_base_peak
    ).astype(np.int32)

    # T wave
    t_on = qrs_on + qrs_w + st_dur
    out_arr[t_on : t_on + t_dur] = get_peak(t_dur, t_amp)
    return out_arr


def get_synthetic_ecg(n_sec: int = 10) -> np.ndarray:
    """Create synthetic ECG."""
    beat = get_ecg_beat()
    return np.tile(beat, n_sec)


def get_peak(width: int, amp: int) -> np.ndarray:
    """Returns a single sinusoidal peak."""
    return amp / 2 * (-np.cos(2 * np.pi * np.arange(width) / width) + 1)


if __name__ == "__main__":  # pragma: no cover
    peak_sig = get_synthetic_ecg()

    import matplotlib.pyplot as plt

    plt.plot(peak_sig)
    plt.show()
