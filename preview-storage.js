/* Hosting-only save isolation. Never writes or removes the public game's keys.
   Copy raw primary and backup only on the first visit to this PR playtest.
   Game.recover keeps its existing validation and paused-market recovery rules. */
(function () {
  const keys = ["mgg10", "mgg10-backup"];
  try {
    if (keys.some(key => localStorage.getItem("mgg-pr-1:" + key) !== null)) return;
    for (const key of keys) {
      const raw = localStorage.getItem(key);
      if (raw !== null) localStorage.setItem("mgg-pr-1:" + key, raw);
    }
  } catch {
    // Existing game save-warning handling remains responsible for storage errors.
  }
})();
