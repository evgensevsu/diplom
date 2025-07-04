if (!window.jdoodleEmbeds) {
  window.jdoodleEmbeds = {};
}

var elements = document.querySelectorAll('[data-pym-src]:not([data-pym-auto-initialized])');
var length = elements.length;

function extractLanguageVersionAndLibs() {
  window.jdoodleEmbeds[element.id].clientId = element.dataset['clientId'];
  window.jdoodleEmbeds[element.id].language = element.dataset['language'];
  window.jdoodleEmbeds[element.id].versionIndex = element.dataset['versionIndex'];
  window.jdoodleEmbeds[element.id].libs = element.dataset['libs'];
  window.jdoodleEmbeds[element.id].hasFiles = element.dataset['hasFiles'];
}

for (var idx = 0; idx < length; ++idx) {
  var element = elements[idx];

  if (element.id === '') {
    element.id = 'pym-' + idx + '-' + Math.random().toString(36).substr(2, 5);
  }

  window.jdoodleEmbeds[element.id] = {};
  if (element.dataset['hasFiles'] === 'true') {
    window.jdoodleEmbeds[element.id].script = element.querySelector('[data-type=script]').textContent;
    window.jdoodleEmbeds[element.id].files = [];
    window.jdoodleEmbeds[element.id].files[0] = {};
    window.jdoodleEmbeds[element.id].files[0].content = element.querySelector('[data-type=file]').textContent;
    window.jdoodleEmbeds[element.id].files[0].name = element.querySelector('[data-type=file]').dataset['fileName'];
  } else {
    window.jdoodleEmbeds[element.id].script = element.textContent;
  }

  extractLanguageVersionAndLibs();

  if (element.dataset['pymSrc'].indexOf('?') > 1) {
    element.dataset['pymSrc'] = element.dataset['pymSrc'] + '&id=' + element.id;
  } else {
    element.dataset['pymSrc'] = element.dataset['pymSrc'] + '?id=' + element.id;
  }
}

/*! pym.js - v1.3.2 - 2018-02-13 */
!(function (a) {
  'function' == typeof define && define.amd
    ? define(a)
    : 'undefined' != typeof module && module.exports
    ? (module.exports = a())
    : (window.pym = a.call(this))
})(function () {
  var a = {},
    b = function (a) {
      var b = document.createEvent('Event');
      b.initEvent('pym:' + a, !0, !0), document.dispatchEvent(b);
    },
    c = function (a) {
      var b = new RegExp('[\\?&]' + a.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]') + '=([^&#]*)'),
        c = b.exec(location.search);
      return null === c ? '' : decodeURIComponent(c[1].replace(/\+/g, ' '));
    },
    d = function (a, b) {
      if (
        ('*' === b.xdomain || a.origin.match(new RegExp(b.xdomain + '$'))) &&
        'string' == typeof a.data
      )
        return !0;
    },
    e = function (a) {
      var b = /^(?:(?:https?|mailto|ftp):|[^&:\/?#]*(?:[\/?#]|$))/gi;
      if (a.match(b)) return !0;
    },
    f = function (a, b, c) {
      return ['pym', a, b, c].join('xPYMx');
    },
    g = function (a) {
      var b = ['pym', a, '(\\S+)', '(.*)'];
      return new RegExp('^' + b.join('xPYMx') + '$');
    },
    h =
      Date.now ||
      function () {
        return new Date().getTime();
      },
    i = function (a, b, c) {
      var d,
        e,
        f,
        g = null,
        i = 0;
      c || (c = {});
      var j = function () {
        ;(i = !1 === c.leading ? 0 : h()), (g = null), (f = a.apply(d, e)), g || (d = e = null);
      };
      return function () {
        var k = h();
        i || !1 !== c.leading || (i = k);
        var l = b - (k - i);
        return (
          (d = this),
          (e = arguments),
          l <= 0 || l > b
            ? (g && (clearTimeout(g), (g = null)),
              (i = k),
              (f = a.apply(d, e)),
              g || (d = e = null))
            : g || !1 === c.trailing || (g = setTimeout(j, l)),
          f
        );
      };
    },
    j = function () {
      for (var b = a.autoInitInstances.length, c = b - 1; c >= 0; c--) {
        var d = a.autoInitInstances[c];
        ;(d.el.getElementsByTagName('iframe').length &&
          d.el.getElementsByTagName('iframe')[0].contentWindow) ||
          a.autoInitInstances.splice(c, 1);
      }
    };
  return (
    (a.autoInitInstances = []),
    (a.autoInit = function (c) {
      var d = document.querySelectorAll('[data-pym-src]:not([data-pym-auto-initialized])'),
        e = d.length;
      j();
      for (var f = 0; f < e; ++f) {
        var g = d[f];
        g.setAttribute('data-pym-auto-initialized', ''),
          '' === g.id && (g.id = 'pym-' + f + '-' + Math.random().toString(36).substr(2, 5));
        var h = g.getAttribute('data-pym-src'),
          i = {
            xdomain: 'string',
            title: 'string',
            name: 'string',
            id: 'string',
            sandbox: 'string',
            allowfullscreen: 'boolean',
            parenturlparam: 'string',
            parenturlvalue: 'string',
            optionalparams: 'boolean',
            trackscroll: 'boolean',
            scrollwait: 'number'
          },
          k = {};
        for (var l in i)
          if (null !== g.getAttribute('data-pym-' + l))
            switch (i[l]) {
              case 'boolean':
                k[l] = !('false' === g.getAttribute('data-pym-' + l));
                break;
              case 'string':
                k[l] = g.getAttribute('data-pym-' + l);
                break;
              case 'number':
                var m = Number(g.getAttribute('data-pym-' + l));
                isNaN(m) || (k[l] = m);
                break;
              default:
                console.err('unrecognized attribute type');
            }
        var n = new a.Parent(g.id, h, k);
        a.autoInitInstances.push(n);
      }
      return c || b('pym-initialized'), a.autoInitInstances;
    }),
    (a.Parent = function (a, b, c) {
      ;(this.id = a),
        (this.url = b),
        (this.el = document.getElementById(a)),
        (this.iframe = null),
        (this.settings = {
          xdomain: '*',
          optionalparams: !0,
          parenturlparam: 'parentUrl',
          parenturlvalue: window.location.href,
          trackscroll: !1,
          scrollwait: 100
        }),
        (this.messageRegex = g(this.id)),
        (this.messageHandlers = {}),
        (c = c || {}),
        (this._constructIframe = function () {
          var a = this.el.offsetWidth.toString();
          this.iframe = document.createElement('iframe');
          var b = '',
            c = this.url.indexOf('#');
          for (
            c > -1 &&
              ((b = this.url.substring(c, this.url.length)), (this.url = this.url.substring(0, c))),
              this.url.indexOf('?') < 0 ? (this.url += '?') : (this.url += '&'),
              (this.iframe.src = this.url + 'initialWidth=' + a + '&childId=' + this.id),
              this.settings.optionalparams &&
                ((this.iframe.src += '&parentTitle=' + encodeURIComponent(document.title)),
                (this.iframe.src +=
                  '&' +
                  this.settings.parenturlparam +
                  '=' +
                  encodeURIComponent(this.settings.parenturlvalue))),
              this.iframe.src += b,
              this.iframe.setAttribute('width', '100%'),
              this.iframe.setAttribute('scrolling', 'no'),
              this.iframe.setAttribute('marginheight', '0'),
              this.iframe.setAttribute('frameborder', '0'),
              this.settings.title && this.iframe.setAttribute('title', this.settings.title),
              void 0 !== this.settings.allowfullscreen &&
                !1 !== this.settings.allowfullscreen &&
                this.iframe.setAttribute('allowfullscreen', ''),
              void 0 !== this.settings.sandbox &&
                'string' == typeof this.settings.sandbox &&
                this.iframe.setAttribute('sandbox', this.settings.sandbox),
              this.settings.id &&
                (document.getElementById(this.settings.id) ||
                  this.iframe.setAttribute('id', this.settings.id)),
              this.settings.name && this.iframe.setAttribute('name', this.settings.name);
            this.el.firstChild;

          )
            this.el.removeChild(this.el.firstChild);
          this.el.appendChild(this.iframe),
            window.addEventListener('resize', this._onResize),
            this.settings.trackscroll && window.addEventListener('scroll', this._throttleOnScroll);
        }),
        (this._onResize = function () {
          this.sendWidth(), this.settings.trackscroll && this.sendViewportAndIFramePosition();
        }.bind(this)),
        (this._onScroll = function () {
          this.sendViewportAndIFramePosition();
        }.bind(this)),
        (this._fire = function (a, b) {
          if (a in this.messageHandlers)
            for (var c = 0; c < this.messageHandlers[a].length; c++)
              this.messageHandlers[a][c].call(this, b);
        }),
        (this.remove = function () {
          window.removeEventListener('message', this._processMessage),
            window.removeEventListener('resize', this._onResize),
            this.el.removeChild(this.iframe),
            j();
        }),
        (this._processMessage = function (a) {
          if (d(a, this.settings) && 'string' == typeof a.data) {
            var b = a.data.match(this.messageRegex);
            if (!b || 3 !== b.length) return !1;
            var c = b[1],
              e = b[2];
            this._fire(c, e);
          }
        }.bind(this)),
        (this._onHeightMessage = function (a) {
          var b = parseInt(a);
          this.iframe.setAttribute('height', b + 'px');
        }),
        (this._onNavigateToMessage = function (a) {
          e(a) && (document.location.href = a);
        }),
        (this._onScrollToChildPosMessage = function (a) {
          var b = document.getElementById(this.id).getBoundingClientRect().top + window.pageYOffset,
            c = b + parseInt(a);
          window.scrollTo(0, c);
        }),
        (this.onMessage = function (a, b) {
          a in this.messageHandlers || (this.messageHandlers[a] = []),
            this.messageHandlers[a].push(b);
        }),
        (this.sendMessage = function (a, b) {
          this.el.getElementsByTagName('iframe').length &&
            (this.el.getElementsByTagName('iframe')[0].contentWindow
              ? this.el
                  .getElementsByTagName('iframe')[0]
                  .contentWindow.postMessage(f(this.id, a, b), '*')
              : this.remove());
        }),
        (this.sendWidth = function () {
          var a = this.el.offsetWidth.toString();
          this.sendMessage('width', a);
        }),
        (this.sendViewportAndIFramePosition = function () {
          var a = this.iframe.getBoundingClientRect(),
            b = window.innerWidth || document.documentElement.clientWidth,
            c = window.innerHeight || document.documentElement.clientHeight,
            d = b + ' ' + c;
          (d += ' ' + a.top + ' ' + a.left),
            (d += ' ' + a.bottom + ' ' + a.right),
            this.sendMessage('viewport-iframe-position', d);
        })
      for (var h in c) this.settings[h] = c[h];
      return (
        (this._throttleOnScroll = i(this._onScroll.bind(this), this.settings.scrollwait)),
        this.onMessage('height', this._onHeightMessage),
        this.onMessage('navigateTo', this._onNavigateToMessage),
        this.onMessage('scrollToChildPos', this._onScrollToChildPosMessage),
        this.onMessage('parentPositionInfo', this.sendViewportAndIFramePosition),
        window.addEventListener('message', this._processMessage, !1),
        this._constructIframe(),
        this
      );
    });
    'undefined' != typeof document && a.autoInit(!0);
    a;
}
