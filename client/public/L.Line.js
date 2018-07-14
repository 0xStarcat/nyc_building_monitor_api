;(function(v) {
  function H(a) {
    for (var b = s + l, c = m + p, d = 0, n = a.length; d < n; d++)
      if (a[d].x > l && a[d].x < b && a[d].y > p && a[d].y < c) return !0
    return !1
  }
  function C(a) {
    w = I + a.x
    x = m + a.y
    f.render(!0)
  }
  function J(a) {
    s = a.width
    m = a.height
    w = I = (s / 2) << 0
    x = m
    f.setSize(s, m)
  }
  function K(a) {
    q = a
    D = Q << q
    t = M(0.95, q - u)
    E = '' + y.alpha(t)
    N = 6 / M(2, q - u)
  }
  var k = Math,
    R = k.log,
    S = k.tan,
    T = k.min,
    U = k.max,
    M = k.pow,
    k = /iP(ad|hone|od)/g.test(navigator.userAgent),
    e = !!~navigator.userAgent.indexOf('Trident'),
    V =
      !v.requestAnimationFrame || k || e
        ? function(a) {
            a()
          }
        : v.requestAnimationFrame,
    F = (function(a) {
      function b(a, b, c) {
        0 > c && (c += 1)
        1 < c && (c -= 1)
        return c < 1 / 6 ? a + 6 * (b - a) * c : 0.5 > c ? b : c < 2 / 3 ? a + (b - a) * (2 / 3 - c) * 6 : a
      }
      var c = {
          aqua: '#00ffff',
          black: '#000000',
          blue: '#0000ff',
          fuchsia: '#ff00ff',
          gray: '#808080',
          grey: '#808080',
          green: '#008000',
          lime: '#00ff00',
          maroon: '#800000',
          navy: '#000080',
          olive: '#808000',
          orange: '#ffa500',
          purple: '#800080',
          red: '#ff0000',
          silver: '#c0c0c0',
          teal: '#008080',
          white: '#ffffff',
          yellow: '#ffff00'
        },
        d = function(a, b, c, d) {
          this.H = a
          this.S = b
          this.L = c
          this.A = d
        }
      d.parse = function(a) {
        var b = 0,
          d = 0,
          g = 0,
          e = 1,
          h
        a = ('' + a).toLowerCase()
        a = c[a] || a
        if ((h = a.match(/^#(\w{2})(\w{2})(\w{2})$/)))
          (b = parseInt(h[1], 16)), (d = parseInt(h[2], 16)), (g = parseInt(h[3], 16))
        else if ((h = a.match(/rgba?\((\d+)\D+(\d+)\D+(\d+)(\D+([\d.]+))?\)/)))
          (b = parseInt(h[1], 10)),
            (d = parseInt(h[2], 10)),
            (g = parseInt(h[3], 10)),
            (e = h[4] ? parseFloat(h[5]) : 1)
        else return
        return this.fromRGBA(b, d, g, e)
      }
      d.fromRGBA = function(a, b, c, g) {
        'object' === typeof a
          ? ((b = a.g / 255), (c = a.b / 255), (g = a.a), (a = a.r / 255))
          : ((a /= 255), (b /= 255), (c /= 255))
        var e = Math.max(a, b, c),
          h = Math.min(a, b, c),
          f,
          k = (e + h) / 2,
          l = e - h
        if (l) {
          h = 0.5 < k ? l / (2 - e - h) : l / (e + h)
          switch (e) {
            case a:
              f = (b - c) / l + (b < c ? 6 : 0)
              break
            case b:
              f = (c - a) / l + 2
              break
            case c:
              f = (a - b) / l + 4
          }
          f *= 60
        } else f = h = 0
        return new d(f, h, k, g)
      }
      d.prototype = {
        toRGBA: function() {
          var a = Math.min(360, Math.max(0, this.H)),
            c = Math.min(1, Math.max(0, this.S)),
            d = Math.min(1, Math.max(0, this.L)),
            g = Math.min(1, Math.max(0, this.A)),
            e
          if (0 === c) a = e = c = d
          else {
            var h = 0.5 > d ? d * (1 + c) : d + c - d * c,
              d = 2 * d - h,
              a = a / 360,
              c = b(d, h, a + 1 / 3)
            e = b(d, h, a)
            a = b(d, h, a - 1 / 3)
          }
          return {
            r: Math.round(255 * c),
            g: Math.round(255 * e),
            b: Math.round(255 * a),
            a: g
          }
        },
        toString: function() {
          var a = this.toRGBA()
          return 1 === a.a
            ? '#' + (16777216 + (a.r << 16) + (a.g << 8) + a.b).toString(16).slice(1, 7)
            : 'rgba(' + [a.r, a.g, a.b, a.a.toFixed(2)].join() + ')'
        },
        hue: function(a) {
          return new d(this.H * a, this.S, this.L, this.A)
        },
        saturation: function(a) {
          return new d(this.H, this.S * a, this.L, this.A)
        },
        lightness: function(a) {
          return new d(this.H, this.S, this.L * a, this.A)
        },
        alpha: function(a) {
          return new d(this.H, this.S, this.L, this.A * a)
        }
      }
      return d
    })(this),
    G = Math.PI,
    W = G / 2,
    X = G / 4,
    Q = 256,
    q,
    D,
    u = 15,
    s = 0,
    m = 0,
    I = 0,
    l = 0,
    p = 0,
    y = F.parse('rgba(200, 190, 180)'),
    E = '' + y,
    t = 1,
    N = 1,
    w,
    x,
    z,
    Y = (function() {
      return {
        read: function(a) {
          if (!a || 'FeatureCollection' !== a.type) return []
          a = a.features
          var b,
            c,
            d = [],
            n,
            e
          b = 0
          for (c = a.length; b < c; b++)
            if (((n = a[b]), 'Feature' === n.type && !1 !== O(n))) {
              e = n.properties
              e.coordinates = n.geometry.coordinates
              if (n.id || n.properties.id) e.id = n.id || n.properties.id
              d.push(e)
            }
          return d
        }
      }
    })(),
    r = {
      items: [],
      getPixelCoordinates: function(a) {
        for (var b = [], c, d = 0, e = a.length; d < e; d++) {
          c = a[d][0]
          var f = T(1, U(0, 0.5 - R(S(X + (W * a[d][1]) / 180)) / G / 2))
          c = { x: ((c / 360 + 0.5) * D) << 0, y: (f * D) << 0 }
          c.z = a[d][2] / N
          b[d] = c
        }
        return b
      },
      resetItems: function() {
        this.items = []
      },
      addRenderItems: function(a) {
        for (var b, c = Y.read(a), d = 0, e = c.length; d < e; d++)
          (a = c[d]), (b = this.scale(a)) && this.items.push(b)
        f.render()
      },
      scale: function(a) {
        var b = {}
        a.id && (b.id = a.id)
        b.coordinates = this.getPixelCoordinates(a.coordinates)
        if ((a = F.parse(a.color || E))) (a = a.alpha(t)), (b.altColor = '' + a.lightness(0.7)), (b.color = '' + a)
        return b
      },
      set: function(a) {
        this.resetItems()
        this._staticData = a
        this.addRenderItems(this._staticData)
      },
      update: function() {
        this.resetItems()
        q < u || this.addRenderItems(this._staticData)
      }
    },
    P = {
      draw: function(a, b) {
        this.extrude(a, b)
      },
      extrude: function(a, b) {
        for (
          var c = b.coordinates, d = { x: 0, y: 0, z: 0 }, e = { x: 0, y: 0, z: 0 }, f, k, g = 0, m = c.length - 1;
          g < m;
          g++
        )
          (d.x = c[g].x - l),
            (d.y = c[g].y - p),
            (d.z = c[g].z),
            (e.x = c[g + 1].x - l),
            (e.y = c[g + 1].y - p),
            (e.z = c[g + 1].z),
            (f = A.project(d, 450 / (450 - d.z))),
            (k = A.project(e, 450 / (450 - e.z))),
            (a.fillStyle = (d.x < e.x && d.y < e.y) || (d.x > e.x && d.y > e.y) ? b.altColor : b.color),
            a.beginPath(),
            this.polygon(a, [e, d, f, k]),
            a.closePath(),
            a.stroke(),
            a.fill()
      },
      polygon: function(a, b) {
        a.moveTo(b[0].x, b[0].y)
        for (var c = 1; c < b.length; c++) a.lineTo(b[c].x, b[c].y)
      },
      shadow: function(a, b) {
        for (var c = b.coordinates, d = { x: 0, y: 0 }, e = { x: 0, y: 0 }, f, k, g = 0, m = c.length - 1; g < m; g++)
          (d.x = c[g].x - l),
            (d.y = c[g].y - p),
            (d.z = c[g].z),
            (e.x = c[g + 1].x - l),
            (e.y = c[g + 1].y - p),
            (e.z = c[g + 1].z),
            (f = B.project(d, d.z)),
            (k = B.project(e, e.z)),
            a.beginPath(),
            a.moveTo(d.x, d.y),
            a.lineTo(f.x, f.y),
            a.lineTo(k.x, k.y),
            a.lineTo(e.x, e.y),
            a.closePath(),
            a.fill()
      }
    },
    A = {
      project: function(a, b) {
        return { x: ((a.x - w) * b + w) << 0, y: ((a.y - x) * b + x) << 0 }
      },
      render: function() {
        var a = this.context
        a.clearRect(0, 0, s, m)
        if (!(q < u || z)) for (var b = r.items, c = 0, d = b.length; c < d; c++) H(b[c].coordinates) && P.draw(a, b[c])
      }
    },
    B = {
      enabled: !0,
      direction: { x: 2, y: 2 },
      project: function(a, b) {
        return { x: a.x + this.direction.x * b, y: a.y + this.direction.y * b }
      },
      render: function() {
        var a = this.context
        a.clearRect(0, 0, s, m)
        if (!(q < u || z)) {
          var b,
            c,
            d = r.items
          a.fillStyle = '#000000'
          a.canvas.style.opacity = 0.4 / (2 * t)
          b = 0
          for (c = d.length; b < c; b++) H(d[b].coordinates) && P.shadow(a, d[b])
        }
      }
    },
    f = {
      container: document.createElement('DIV'),
      items: [],
      init: function() {
        this.container.style.pointerEvents = 'none'
        this.container.style.position = 'absolute'
        this.container.style.left = 0
        this.container.style.top = 0
        B.context = this.createContext(this.container)
        A.context = this.createContext(this.container)
        this.createContext(this.container)
      },
      render: function(a) {
        V(function() {
          a || B.render()
          A.render()
        })
      },
      createContext: function(a) {
        var b = document.createElement('CANVAS')
        b.style.webkitTransform = 'translate3d(0,0,0)'
        b.style.imageRendering = 'optimizeSpeed'
        b.style.position = 'absolute'
        b.style.left = 0
        b.style.top = 0
        var c = b.getContext('2d')
        c.lineCap = 'round'
        c.lineJoin = 'round'
        c.lineWidth = 1
        c.mozImageSmoothingEnabled = !1
        c.webkitImageSmoothingEnabled = !1
        this.items.push(b)
        a && a.appendChild(b)
        return c
      },
      appendTo: function(a) {
        a.appendChild(this.container)
      },
      remove: function() {
        this.container.parentNode.removeChild(this.container)
      },
      setSize: function(a, b) {
        for (var c = 0, d = this.items.length; c < d; c++) (this.items[c].width = a), (this.items[c].height = b)
      },
      setPosition: function(a, b) {
        this.container.style.left = a + 'px'
        this.container.style.top = b + 'px'
      }
    }
  f.init()
  k = function(a) {
    this.offset = { x: 0, y: 0 }
    r.set(a)
  }
  e = k.prototype = L.Layer ? new L.Layer() : {}
  e.addTo = function(a) {
    a.addLayer(this)
  }
  e.onAdd = function(a) {
    this.map = a
    f.appendTo(a._panes.overlayPane)
    var b = this.getOffset(),
      c = a.getPixelOrigin()
    J({ width: a._size.x, height: a._size.y })
    var d = c.y - b.y
    l = c.x - b.x
    p = d
    K(a._zoom)
    f.setPosition(-b.x, -b.y)
    a.on(
      {
        move: this.onMove,
        moveend: this.onMoveEnd,
        zoomstart: this.onZoomStart,
        zoomend: this.onZoomEnd,
        resize: this.onResize,
        viewreset: this.onViewReset,
        click: this.onClick
      },
      this
    )
    if (a.options.zoomAnimation) a.on('zoomanim', this.onZoom, this)
    r.update()
  }
  e.onRemove = function() {
    var a = this.map
    a.off(
      {
        move: this.onMove,
        moveend: this.onMoveEnd,
        zoomstart: this.onZoomStart,
        zoomend: this.onZoomEnd,
        resize: this.onResize,
        viewreset: this.onViewReset,
        click: this.onClick
      },
      this
    )
    a.options.zoomAnimation && a.off('zoomanim', this.onZoom, this)
    f.remove()
  }
  e.onMove = function(a) {
    a = this.getOffset()
    C({ x: this.offset.x - a.x, y: this.offset.y - a.y })
  }
  e.onMoveEnd = function(a) {
    if (this.noMoveEnd) this.noMoveEnd = !1
    else {
      var b = this.map
      a = this.getOffset()
      var c = b.getPixelOrigin()
      this.offset = a
      f.setPosition(-a.x, -a.y)
      C({ x: 0, y: 0 })
      J({ width: b._size.x, height: b._size.y })
      b = c.y - a.y
      l = c.x - a.x
      p = b
      f.render()
      r.update()
    }
  }
  e.onZoomStart = function(a) {
    z = !0
    f.render()
  }
  e.onZoom = function(a) {}
  e.onZoomEnd = function(a) {
    a = this.map
    var b = this.getOffset(),
      c = a.getPixelOrigin(),
      d = c.y - b.y
    l = c.x - b.x
    p = d
    a = a._zoom
    z = !1
    K(a)
    r.update()
    f.render()
    this.noMoveEnd = !0
  }
  e.onResize = function() {}
  e.onViewReset = function() {
    var a = this.getOffset()
    this.offset = a
    f.setPosition(-a.x, -a.y)
    C({ x: 0, y: 0 })
  }
  e.getOffset = function() {
    return L.DomUtil.getPosition(this.map._mapPane)
  }
  e.style = function(a) {
    a = a || {}
    if ((a = a.color)) (y = F.parse(a).alpha(t)), (E = '' + y)
    f.render()
    return this
  }
  e.set = function(a) {
    r.set(a)
    return this
  }
  var O = function() {}
  e.each = function(a) {
    O = function(b) {
      return a(b)
    }
    return this
  }
  k.VERSION = '0.1.0'
  v.L && (v.L.Line3 = k)
})(this)
