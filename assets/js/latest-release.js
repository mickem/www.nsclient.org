(function () {
  // Captured while the script is executing; used to resolve /data/*.json from
  // any page depth (the home page is at the root, /download/ is not).
  var SCRIPT_SRC = (document.currentScript && document.currentScript.src) || '';

  // key -> where to get its releases. `data` is relative to the site root.
  var PROJECTS = {
    nscp: { repo: 'mickem/nscp', data: 'data/releases.json' },
    check_nsclient: { repo: 'mickem/check_nsclient', data: 'data/check_nsclient-releases.json' },
    fleet: { repo: 'mickem/nsclient-fleet-server', data: 'data/fleet-releases.json' }
  };
  var DEFAULT_PROJECT = 'nscp';
  var CACHE_PREFIX = 'nscp-latest-release-v3:';
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

  // GitHub shows binary sizes labelled MB, so do the same.
  function fmtSize(bytes) {
    if (!bytes || bytes <= 0) return '';
    var units = ['B', 'KB', 'MB', 'GB'];
    var n = bytes, i = 0;
    while (n >= 1024 && i < units.length - 1) { n /= 1024; i++; }
    return (i === 0 ? n : n.toFixed(1)) + ' ' + units[i];
  }

  // Assets come trimmed from data/*.json (url) or raw from the GitHub API
  // (browser_download_url) when the build-time data is unavailable.
  function assetUrl(asset) {
    return asset.url || asset.browser_download_url || '';
  }

  // The version placeholder in an asset pattern: <version> in visible text
  // (inside a code span) or $version in a data-release-asset attribute,
  // where Markdown would read <version> as an HTML tag.
  var PLACEHOLDER = /<version>|\$version/g;

  // 'NSCP-$version-x64.msi' -> /^NSCP-(.+?)-x64\.msi$/, so a file is found
  // even when the tag and the version in the file name are spelled apart.
  function assetPattern(template) {
    var parts = template.split(PLACEHOLDER).map(function (part) {
      return part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    });
    return new RegExp('^' + parts.join('(.+?)') + '$');
  }

  function findAsset(release, template, version) {
    var assets = (release && release.assets) || [];
    var exact = template.replace(PLACEHOLDER, version);
    for (var i = 0; i < assets.length; i++) {
      if (assets[i].name === exact) return assets[i];
    }
    var re = assetPattern(template);
    for (var j = 0; j < assets.length; j++) {
      if (re.test(assets[j].name || '')) return assets[j];
    }
    return null;
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

  function applyLatest(release, key, authoritative) {
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
    applyAssets(release, key, version, authoritative);
  }

  // Sits between two links on one line: " · ", " | " or ", ".
  var SEPARATOR = /^\s*[·|,]\s*$/;

  // Take the separator in front of a dropped link with it, or the one behind
  // it when the link was first on the line, so what is left does not start or
  // end with a stray bullet.
  function dropSeparator(el) {
    var before = el.previousSibling;
    if (before && before.nodeType === 3 && SEPARATOR.test(before.nodeValue)) {
      before.parentNode.removeChild(before);
      return;
    }
    var after = el.nextSibling;
    if (after && after.nodeType === 3 && SEPARATOR.test(after.nodeValue)) {
      after.parentNode.removeChild(after);
    }
  }

  // A link marked data-release-optional names a file that not every release
  // carries — a platform added along the way, such as the Windows ARM64 MSI or
  // the Raspberry Pi package. Drop it when the latest release has no such
  // file, rather than leaving it pointing at the release page as if the
  // download existed. The value says what to drop: "self" for the link alone,
  // or a selector for the element around it ("li" when the link is the only
  // thing in its bullet, which would otherwise be left dangling).
  function dropOptional(el) {
    var target = el.getAttribute('data-release-optional');
    if (target && target !== 'self') {
      var around = el.closest(target);
      if (around) {
        around.parentNode.removeChild(around);
        return;
      }
    }
    dropSeparator(el);
    el.parentNode.removeChild(el);
  }

  // Links marked data-release="asset" name a file of the latest release with
  // a placeholder for the version: data-release-asset="NSCP-$version-x64.msi"
  // on a link with its own label ("64-bit"), or the visible text itself,
  // e.g. `NSCP-Web-<version>.zip`, which is then replaced by the real file
  // name. Point each at the matching asset; leave links whose file is not
  // in the release alone, so they keep pointing at the release page — unless
  // they are marked optional, which only a paint from fresh data may drop,
  // since a stale cache could be a release behind the file's arrival.
  function applyAssets(release, key, version, authoritative) {
    elements('asset', key).forEach(function (el) {
      var template = el.getAttribute('data-release-asset');
      if (!template) {
        template = (el.textContent || '').trim();
        // Remember the pattern, and that the label shows the file name,
        // for when a later paint carries a newer release.
        el.setAttribute('data-release-asset', template);
        el.setAttribute('data-release-label', 'name');
      }
      var asset = template && findAsset(release, template, version);
      if (!asset || !assetUrl(asset)) {
        if (authoritative && el.hasAttribute('data-release-optional')) {
          dropOptional(el);
        }
        return;
      }
      el.href = assetUrl(asset);
      if (el.getAttribute('data-release-label') === 'name') {
        (el.querySelector('code') || el).textContent = asset.name;
      }
      var size = fmtSize(asset.size);
      el.title = size ? asset.name + ' (' + size + ')' : asset.name;
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

  // `authoritative` marks a paint from freshly fetched data, as opposed to one
  // from the local cache: only those may drop an optional download link.
  function paint(data, key, authoritative) {
    if (!data) return;
    applyLatest(data.latest || (data.releases && data.releases[0]), key, authoritative);
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
        paint(data, key, true);
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
    return ['version', 'date', 'notes-link', 'download-link', 'asset'].some(function (kind) {
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
