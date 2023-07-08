
let size = {
  width: undefined,
  height: undefined
}
const resize_elm_full = () => {
  
     
  

  const container = document
    .getElementsByClassName('book-viewport')[0]
    .getElementsByClassName('container')[0]

  const book = document.getElementsByClassName('book')[0]
  const animated = document.getElementsByClassName('animated')[0]
  book.style.top = '0'
  book.style.left = '0'
  
  book.style.transform = 'translate(-51%, -50%)'
}
const base_full_screen = full => {
  next_button = document.getElementsByClassName('next-button')[0]
  previous_button = document.getElementsByClassName('previous-button')[0]

  next_button.style.display = 'none'
  previous_button.style.display = 'none'
  
  size = $('.book').turn('size')
  const view = document.getElementById('canvas')
  const new_view = view.cloneNode(true)

  // resizeViewport($(window).width(), $(window).height(), false)

  // $('.book').turn('size', $(window).width(), $(window).height())

  resize_elm_full()

  const fullscreen = document.getElementById('fullscreen')


  

   
  // create new copy (static not dynamic from view to use it in background)
  
  new_view.classList.add('canvas_as_clnm')
  // append new view (static to main-content)
  document.getElementById('main-content').appendChild(new_view)
  
  // append new view (static to main-content ) and remove it from original place
  
  fullscreen.appendChild(view)
  
  // show it
  fullscreen.style.transform = 'scale(1)'

  book_viewport = document.getElementById('book-viewport')
  // const w=$('.book').turn('size').width+'px!important;'
  // const h=$('.book').turn('size').height+'px!important;'  
  const w=$(window).width()+'px'
  const h=$(window).height()+'px'
  
   
  console.log( "wh",w,h)
  $('.book').turn('size',$(window).width(),$(window).height())
  book_viewport.style.width = w
  book_viewport.style.height =h
 

  // book_viewport.style.backgroundColor= 'red'
  
}
const resize_elm_full_back = () => {
  const book = document.getElementsByClassName('book')[0]
  const animated = document.getElementsByClassName('animated')[0]
  book.style.top = '0'
  book.style.left = '0'

  book.style.transform = 'translate(-51%, -48%)'
}
const exit_fullscreen_base = () => {
  // resizeViewport(size.width, size.height, false)
  $('.book').turn('size', size.width, size.height)
  resize_elm_full_back()
  const fullscreen = document.getElementById('fullscreen')

  const main_content = document.getElementById('main-content')
  // remove old  view (static to main-content)

  const view = document.getElementsByClassName('canvas_as_clnm')[0]
  view.remove()

  // append new view (static to main-content ) and remove it from original place

  next_button = document.getElementsByClassName('next-button')[0]
  previous_button = document.getElementsByClassName('previous-button')[0]

  next_button.style.visibility = 'visible'
  previous_button.style.visibility = 'visible'

  main_content.appendChild(document.getElementById('canvas'))
  // show it
  fullscreen.style.transform = 'scale(0)'
}

function addPage(page, book, static) {
  console.log(static_path)
  // if (!static_path)
  // static_path = static
  var id,
    pages = book.turn('pages')

  // Create a new element for this page

  var element = $('<div />', {})
  if (
    page == 1 ||
    page == 2 ||
    page == number_of_pages ||
    page == number_of_pages - 1
  )
    element = $('<div />', {
      class: 'hard'
    })

  // Add the page to the flipbook
  if (book.turn('addPage', element, page)) {
    // Add the initial HTML
    // It will contain a loader indicator and a gradient
    // if (
    //   page === 1 ||
    //   page === 2 ||
    //   page === number_of_pages ||
    //   page === number_of_pages - 1
    // ) {
    //   element.html(
    //     '<div depth="5" className="hard"> <div className="side" /></div> </div>'
    //   );
    // } else
    element.html('<div  class="gradient"></div><div class="loader"></div>')

    // Load the page
    loadPage(page, element)
  }
}

function loadPage(page, pageElement) {
  // Create an image element

  var img = $('<img />')

  img.mousedown(function (e) {
    e.preventDefault()
  })

  img.load(function () {
    // Set the size
    $(this).css({
      width: '100%',
      height: '100%'
    })

    // Add the image to the page after loaded
    // if (
    //   page === 1 ||
    //   page === 2 ||
    //   page === number_of_pages ||
    //   page === number_of_pages - 1
    // )
    //   $(this).insertTo(pageElement );
    // else

    $(this).appendTo(pageElement)

    // Remove the loader indicator

    pageElement.find('.loader').remove()
  })

  // Load the page

  img.attr('src', static_path + '/' + page + '.png')

  //loadRegions(page, pageElement);
}

// Zoom in / Zoom out

function zoomTo(event) {
  setTimeout(function () {
    if ($('.book-viewport').data().regionClicked) {
      $('.book-viewport').data().regionClicked = false
    } else {
      if ($('.book-viewport').zoom('value') == 1) {
        $('.book-viewport').zoom('zoomIn', event)
      } else {
        $('.book-viewport').zoom('zoomOut')
      }
    }
  }, 1)
}

// Load regions

function loadRegions(page, element) {
  $.getJSON('pages/' + page + '-regions.json').done(function (data) {
    $.each(data, function (key, region) {
      addRegion(region, element)
    })
  })
}

// Add region

function addRegion(region, pageElement) {
  var reg = $('<div />', {
      class: 'region  ' + region['class']
    }),
    options = $('.book').turn('options'),
    pageWidth = options.width / 2,
    pageHeight = options.height

  reg
    .css({
      top: Math.round((region.y / pageHeight) * 100) + '%',
      left: Math.round((region.x / pageWidth) * 100) + '%',
      width: Math.round((region.width / pageWidth) * 100) + '%',
      height: Math.round((region.height / pageHeight) * 100) + '%'
    })
    .attr('region-data', $.param(region.data || ''))

  reg.appendTo(pageElement)
}

// Process click on a region

function regionClick(event) {
  var region = $(event.target)

  if (region.hasClass('region')) {
    $('.book-viewport').data().regionClicked = true

    setTimeout(function () {
      $('.book-viewport').data().regionClicked = false
    }, 100)

    var regionType = $.trim(region.attr('class').replace('region', ''))

    return processRegion(region, regionType)
  }
}

// Process the data of every region

function processRegion(region, regionType) {
  data = decodeParams(region.attr('region-data'))

  switch (regionType) {
    case 'link':
      window.open(data.url)

      break
    case 'zoom':
      var regionOffset = region.offset(),
        viewportOffset = $('.book-viewport').offset(),
        pos = {
          x: regionOffset.left - viewportOffset.left,
          y: regionOffset.top - viewportOffset.top
        }

      $('.book-viewport').zoom('zoomIn', pos)

      break
    case 'to-page':
      $('.book').turn('page', data.page)

      break
  }
}

// Load large page

function loadLargePage(page, pageElement) {
  var img = $('<img />')

  img.load(function () {
    var prevImg = pageElement.find('img')
    $(this).css({
      width: '100%',
      height: '100%'
    })
    $(this).appendTo(pageElement)
    prevImg.remove()
  })

  // Loadnew page

  img.attr('src', static_path + '/' + +page + '-large.png')
}

// Load small page

function loadSmallPage(page, pageElement) {
  var img = pageElement.find('img')

  img.css({
    width: '100%',
    height: '100%'
  })

  img.unbind('load')
  // Loadnew page

  img.attr('src', static_path + '/' + page + '.png')
}

// http://code.google.com/p/chromium/issues/detail?id=128488

function isChrome() {
  return navigator.userAgent.indexOf('Chrome') != -1
}

function disableControls(page) {
  if (page == 1) $('.previous-button').hide()
  else $('.previous-button').show()

  if (page == $('.book').turn('pages')) $('.next-button').hide()
  else $('.next-button').show()
}

// Set the width and height for the viewport

function resizeViewport(w, h, z) {
  console.log(w, h)
  var width = w || $(window).width() < 960 ? $(window).width() : undefined,
    // height =  $(window).width() < 960 ?$(window).height() :undefined
    height = h || $(window).width() < 960 ? $(window).height() : '800px'

  console.log(w, h)

  // console.log('$(window).width()',$(window).width())
  // console.log(w,h)
  // var width =$(window).width() < 960 ? $(window).width() : undefined
  // if(w)
  // width = w
  // var height = h || $(window).width() < 960 ? $(window).height() : '800px'
  // if(h)
  //   height = h
  // height =  $(window).width() < 960 ?$(window).height() :undefined

  console.log(w, h)

  // var width = "100%"
  // var  height = "100%"
  options = $('.book').turn('options')

  $('.book').removeClass('animated')

  $('.book-viewport')
    .css({
      width: width,
      height: height
    })
    .zoom('resize')

  if ($('.book').turn('zoom') == 1) {
    var bound = calculateBound({
      width: options.width,
      height: options.height,
      boundWidth: Math.min(options.width, width),
      boundHeight: Math.min(options.height, height)
    })

    if (bound.width % 2 !== 0) bound.width -= 1

    if (
      bound.width != $('.book').width() ||
      bound.height != $('.book').height()
    ) {
      $('.book').turn('size', bound.width, bound.height)

      if ($('.book').turn('page') == 1) $('.book').turn('peel', 'br')

      $('.next-button').css({
        height: bound.height,
        backgroundPosition: '-38px ' + (bound.height / 2 - 32 / 2) + 'px'
      })
      $('.previous-button').css({
        height: bound.height,
        backgroundPosition: '-4px ' + (bound.height / 2 - 32 / 2) + 'px'
      })
    }

    $('.book').css({
      top: -bound.height / 2,
      left: -bound.width / 2
    })
  }

  var bookOffset = $('.book').offset(),
    boundH = height - bookOffset.top - $('.book').height(),
    marginTop = (boundH - $('.thumbnails > div').height()) / 2

  if (marginTop < 0) {
    $('.thumbnails').css({
      height: 1
    })
  } else {
    $('.thumbnails').css({
      height: boundH
    })
    $('.thumbnails > div').css({
      marginTop: marginTop
    })
  }

  if (bookOffset.top < $('.made').height()) $('.made').hide()
  else $('.made').show()

  $('.book').addClass('animated')
}

// Number of views in a flipbook

function numberOfViews(book) {
  return book.turn('pages') / 2 + 1
}

// Current view in a flipbook

function getViewNumber(book, page) {
  return parseInt((page || book.turn('page')) / 2 + 1, 10)
}

function moveBar(yes) {
  if (Modernizr && Modernizr.csstransforms) {
    $('#slider .ui-slider-handle').css({
      zIndex: yes ? -1 : 10000
    })
  }
}

function setPreview(view) {
  var previewWidth = 112,
    previewHeight = 73,
    previewSrc = 'pages/preview.jpg',
    preview = $(_thumbPreview.children(':first')),
    numPages =
    view == 1 || view == $('#slider').slider('option', 'max') ? 1 : 2,
    width = numPages == 1 ? previewWidth / 2 : previewWidth

  _thumbPreview.addClass('no-transition').css({
    width: width + 15,
    height: previewHeight + 15,
    top: -previewHeight - 30,
    left: ($($('#slider').children(':first')).width() - width - 15) / 2
  })

  preview.css({
    width: width,
    height: previewHeight
  })

  if (
    preview.css('background-image') === '' ||
    preview.css('background-image') == 'none'
  ) {
    preview.css({
      backgroundImage: 'url(' + previewSrc + ')'
    })

    setTimeout(function () {
      _thumbPreview.removeClass('no-transition')
    }, 0)
  }

  preview.css({
    backgroundPosition: '0px -' + (view - 1) * previewHeight + 'px'
  })
}

// Width of the flipbook when zoomed in

function largeBookWidth() {
  return 2214
}

// decode URL Parameters

function decodeParams(data) {
  var parts = data.split('&'),
    d,
    obj = {}

  for (var i = 0; i < parts.length; i++) {
    d = parts[i].split('=')
    obj[decodeURIComponent(d[0])] = decodeURIComponent(d[1])
  }

  return obj
}

// Calculate the width and height of a square within another square

function calculateBound(d) {
  var bound = {
    width: d.width,
    height: d.height
  }

  if (bound.width > d.boundWidth || bound.height > d.boundHeight) {
    var rel = bound.width / bound.height

    if (
      d.boundWidth / rel > d.boundHeight &&
      d.boundHeight * rel <= d.boundWidth
    ) {
      bound.width = Math.round(d.boundHeight * rel)
      bound.height = d.boundHeight
    } else {
      bound.width = d.boundWidth
      bound.height = Math.round(d.boundWidth / rel)
    }
  }

  return bound
}