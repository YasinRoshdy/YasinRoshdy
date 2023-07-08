 
var numberOfPages_quran = 10;


  // Adds the pages that the book will need
  function addPage(page, book) {
      // 	First check if the page is already in the book
      if (!book.turn('hasPage', page)) {
          // Create an element for this page
          //page_name = "images/quran/" + page + ".png"
          var element = $('<div />', {
              'class': 'page ' + ((page % 2 == 0) ? 'odd' : 'even'),
              'id': 'page-' + page,
              style: "background-image:url({% static 'images/quran/' + page + '.png' %});"
          }).html('<i class="loader"></i>');
          // If not then add the page
          book.turn('addPage', element, page);
          // Let's assum that the data is comming from the server and the request takes 1s.

          // setTimeout(function () {
          // 	element.html('<div class="data">Data for page ' + page + '</div>');
          // 	}, 1000);


      }
  }

  
  $('#number-pages').html(numberOfPages_quran);

  $('#page-number').keydown(function (e) {

      if (e.keyCode == 13)
          $('#book').turn('page', $('#page-number').val());

  });
  $(window).bind('keydown', function (e) {

      if (e.keyCode == 37)
          $('#quran').turn('previous');
      else if (e.keyCode == 39)
          $('#quran').turn('next');

  });
  $(window).ready(function () {
    $('#quran').turn($,{
        pages: numberOfPages_quran,
        display: 'double',
        acceleration: true,
        gradients: !$.isTouch,
        elevation: 50,
        when: {
            turned: function (e, page) {
                $('#page-number').val(page);
                /*console.log('Current view: ', $(this).turn('view'));*/
            },
            turning: function (e, page, view) {

                // Gets the range of pages that the book needs right now
                var range = $(this).turn('range', page);

                // Check if each page is within the book
                console.log("range[1]", range[1])
                for (page = range[0]; page <= range[1]; page++)
                    addPage(page, $(this));

            },
        }
    });
});
