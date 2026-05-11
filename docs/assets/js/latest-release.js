(function () {
  var REPO = 'mickem/nscp';
  var CACHE_KEY = 'nscp-latest-release-v1';
  var CACHE_TTL_MS = 60 * 60 * 1000;

  function fmtDate(iso) {
    if (!iso) return '';
    try {
      return new Date(iso).toLocaleDateString(undefined, {
        year: 'numeric', month: 'short', day: 'numeric'
      });
    } catch (e) { return ''; }
  }

  function cleanTag(s) {
    return (s || '').replace(/^v/i, '');
  }

  function firstMeaningfulLine(body) {
    var lines = (body || '').split(/\r?\n/);
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!line) continue;
      line = line.replace(/^#+\s*/, '');
      line = line.replace(/^[-*]\s*/, '');
      if (line.length > 0) return line;
    }
    return '';
  }

  function applyLatest(release) {
    if (!release) return;
    var version = cleanTag(release.tag_name || release.name);
    var date = fmtDate(release.published_at);
    var url = release.html_url || 'https://github.com/' + REPO + '/releases/latest';

    document.querySelectorAll('[data-release="version"]').forEach(function (el) {
      el.textContent = version || 'latest';
    });
    document.querySelectorAll('[data-release="date"]').forEach(function (el) {
      el.textContent = date;
    });
    document.querySelectorAll('[data-release="notes-link"]').forEach(function (el) {
      el.href = url;
    });
    document.querySelectorAll('[data-release="download-link"]').forEach(function (el) {
      el.href = url;
    });
  }

  function renderReleases(releases) {
    var container = document.getElementById('nscp-releases');
    if (!container) return;
    if (!releases || !releases.length) return;
    container.replaceChildren();

    releases.slice(0, 3).forEach(function (r) {
      var item = document.createElement('article');
      item.className = 'release-item';

      var header = document.createElement('div');
      header.className = 'release-header';

      var link = document.createElement('a');
      link.className = 'release-title';
      link.href = r.html_url || '#';
      link.textContent = cleanTag(r.name || r.tag_name) || 'release';

      var date = document.createElement('span');
      date.className = 'release-date';
      date.textContent = fmtDate(r.published_at);

      header.appendChild(link);
      header.appendChild(date);

      var summary = document.createElement('p');
      summary.className = 'release-summary';
      var line = firstMeaningfulLine(r.body);
      if (line.length > 200) line = line.slice(0, 200).trim() + '…';
      summary.textContent = line;

      item.appendChild(header);
      if (line) item.appendChild(summary);
      container.appendChild(item);
    });
  }

  function loadCache() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || !parsed.ts) return null;
      if (Date.now() - parsed.ts > CACHE_TTL_MS) return null;
      return parsed.data;
    } catch (e) { return null; }
  }

  function saveCache(data) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({ ts: Date.now(), data: data }));
    } catch (e) {}
  }

  function paint(data) {
    if (!data) return;
    applyLatest(data.latest || (data.releases && data.releases[0]));
    renderReleases(data.releases);
  }

  function showFallback(message) {
    var container = document.getElementById('nscp-releases');
    if (!container) return;
    if (container.querySelector('.release-item')) return;
    container.replaceChildren();
    var p = document.createElement('p');
    p.className = 'release-loading';
    var link = document.createElement('a');
    link.href = 'https://github.com/' + REPO + '/releases';
    link.textContent = 'See all releases on GitHub';
    p.appendChild(document.createTextNode(message + ' '));
    p.appendChild(link);
    container.appendChild(p);
  }

  function fetchLocal() {
    return fetch('data/releases.json', { cache: 'no-cache' })
      .then(function (r) {
        if (!r.ok) throw new Error('local releases.json: ' + r.status);
        return r.json();
      });
  }

  function fetchGithub() {
    return fetch('https://api.github.com/repos/' + REPO + '/releases?per_page=15', {
      headers: { 'Accept': 'application/vnd.github+json' }
    }).then(function (r) {
      if (!r.ok) throw new Error('GitHub API: ' + r.status);
      return r.json();
    }).then(function (releases) {
      return releases.filter(function (r) { return !r.prerelease && !r.draft; });
    });
  }

  function init() {
    var cached = loadCache();
    if (cached) paint(cached);

    fetchLocal()
      .catch(function (localErr) {
        if (window.console && console.info) {
          console.info('latest-release: no build-time data (' + localErr.message + '), falling back to GitHub API');
        }
        return fetchGithub();
      })
      .then(function (releases) {
        if (!releases || !releases.length) {
          throw new Error('No releases available');
        }
        var data = { latest: releases[0], releases: releases };
        paint(data);
        saveCache(data);
      })
      .catch(function (err) {
        if (window.console && console.warn) {
          console.warn('latest-release: failed to load releases —', err.message);
        }
        showFallback('Could not load latest releases.');
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
