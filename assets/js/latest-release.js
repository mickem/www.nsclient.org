(function () {
  // Captured while the script is executing; used to resolve /data/*.json from
  // any page depth (the home page is at the root, /download/ is not).
  var SCRIPT_SRC = (document.currentScript && document.currentScript.src) || '';

  // key -> where to get its releases. `data` is relative to the site root.
  var PROJECTS = {
    nscp: { repo: 'mickem/nscp', data: 'data/releases.json' },
    check_nsclient: { repo: 'mickem/check_nsclient', data: 'data/check_nsclient-releases.json' }
  };
  var DEFAULT_PROJECT = 'nscp';
  var CACHE_PREFIX = 'nscp-latest-release-v2:';
  var CACHE_TTL_MS = 60 * 60 * 1000;

  // assets/js/latest-release.js -> the site root, whatever the page depth.
  function siteUrl(path) {
    if (!SCRIPT_SRC) return path;
    try {
      return new URL('../../' + path, SCRIPT_SRC).toString();
    } catch (e) {
      return path;
    }
  }

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

  // Elements opt into a project with data-release-repo; no attribute means the
  // agent, so the original home page markup keeps working unchanged.
  function elements(kind, key) {
    var attr = '[data-release="' + kind + '"]';
    var selector = attr + '[data-release-repo="' + key + '"]';
    if (key === DEFAULT_PROJECT) {
      selector = attr + ':not([data-release-repo]), ' + selector;
    }
    return document.querySelectorAll(selector);
  }

  function applyLatest(release, key) {
    if (!release) return;
    var version = cleanTag(release.tag_name || release.name);
    var date = fmtDate(release.published_at);
    var url = release.html_url ||
      'https://github.com/' + PROJECTS[key].repo + '/releases/latest';

    elements('version', key).forEach(function (el) {
      el.textContent = version || 'latest';
    });
    elements('date', key).forEach(function (el) {
      el.textContent = date;
    });
    elements('notes-link', key).forEach(function (el) {
      el.href = url;
    });
    elements('download-link', key).forEach(function (el) {
      el.href = url;
    });
  }

  function renderReleases(releases, key) {
    var container = document.getElementById(
      key === DEFAULT_PROJECT ? 'nscp-releases' : key + '-releases'
    );
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

  function loadCache(key) {
    try {
      var raw = localStorage.getItem(CACHE_PREFIX + key);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || !parsed.ts) return null;
      if (Date.now() - parsed.ts > CACHE_TTL_MS) return null;
      return parsed.data;
    } catch (e) { return null; }
  }

  function saveCache(key, data) {
    try {
      localStorage.setItem(CACHE_PREFIX + key, JSON.stringify({ ts: Date.now(), data: data }));
    } catch (e) {}
  }

  function paint(data, key) {
    if (!data) return;
    applyLatest(data.latest || (data.releases && data.releases[0]), key);
    renderReleases(data.releases, key);
  }

  function showFallback(key, message) {
    var container = document.getElementById(
      key === DEFAULT_PROJECT ? 'nscp-releases' : key + '-releases'
    );
    if (!container) return;
    if (container.querySelector('.release-item')) return;
    container.replaceChildren();
    var p = document.createElement('p');
    p.className = 'release-loading';
    var link = document.createElement('a');
    link.href = 'https://github.com/' + PROJECTS[key].repo + '/releases';
    link.textContent = 'See all releases on GitHub';
    p.appendChild(document.createTextNode(message + ' '));
    p.appendChild(link);
    container.appendChild(p);
  }

  function fetchLocal(key) {
    var url = siteUrl(PROJECTS[key].data);
    return fetch(url, { cache: 'no-cache' })
      .then(function (r) {
        if (!r.ok) throw new Error(PROJECTS[key].data + ': ' + r.status);
        return r.json();
      });
  }

  function fetchGithub(key) {
    return fetch('https://api.github.com/repos/' + PROJECTS[key].repo + '/releases?per_page=15', {
      headers: { 'Accept': 'application/vnd.github+json' }
    }).then(function (r) {
      if (!r.ok) throw new Error('GitHub API: ' + r.status);
      return r.json();
    }).then(function (releases) {
      return releases.filter(function (r) { return !r.prerelease && !r.draft; });
    });
  }

  function load(key) {
    var cached = loadCache(key);
    if (cached) paint(cached, key);

    return fetchLocal(key)
      .catch(function (localErr) {
        if (window.console && console.info) {
          console.info('latest-release: no build-time data for ' + key +
            ' (' + localErr.message + '), falling back to GitHub API');
        }
        return fetchGithub(key);
      })
      .then(function (releases) {
        if (!releases || !releases.length) {
          throw new Error('No releases available');
        }
        var data = { latest: releases[0], releases: releases };
        paint(data, key);
        saveCache(key, data);
      })
      .catch(function (err) {
        if (window.console && console.warn) {
          console.warn('latest-release: failed to load releases for ' + key + ' —', err.message);
        }
        showFallback(key, 'Could not load latest releases.');
      });
  }

  // Only ask for a project this page actually shows something for.
  function isUsed(key) {
    if (document.getElementById(key === DEFAULT_PROJECT ? 'nscp-releases' : key + '-releases')) {
      return true;
    }
    return ['version', 'date', 'notes-link', 'download-link'].some(function (kind) {
      return elements(kind, key).length > 0;
    });
  }

  function init() {
    Object.keys(PROJECTS).forEach(function (key) {
      if (isUsed(key)) load(key);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
