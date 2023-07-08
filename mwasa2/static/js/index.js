function init() {
  elements = document.getElementsByClassName("ar-text");
  for (element of elements) {
    element.setAttribute("lang", "ar");
  }
}
init();

// const set_elm_source = (text, source_vid, source_aud) => {

//     console.log("text", text)
//     console.log("source_vid", source_vid)
//     console.log("source_aud", source_aud)
//     if (source_vid && source_vid != "") {
//         vid_source = document.getElementById("video-tafsir-source")
//         vid_source.src = source_vid
//     }
//     if (source_aud && source_aud != "") {
//         aud_source = document.getElementById("audio-tafsir-source")
//         aud_source.src = source_aud
//     }
//     if (text && text != "") {
//         aud_source = document.getElementById("text-source")
//         aud_source.innerHTML = text
//     }

// }
// const hide_elm = (elm_id, ) => {

//     elm = document.getElementById(elm_id)
//     elm.hidden = false;
//   }

// const myCustomScrollbar = document.querySelector('.my-custom-scrollbar');
// const ps = new PerfectScrollbar(myCustomScrollbar);

// const scrollbarY = myCustomScrollbar.querySelector('.ps__rail-y');

// myCustomScrollbar.onscroll = function () {
//   scrollbarY.style.cssText = `top: ${this.scrollTop}px!important; height: 400px; right: ${-this.scrollLeft}px`;
// }
const set_data = (text, source_vid, source_aud, source_read) => {
  tafsir_aud_a = document.getElementById("tafsir_aud_a");
  tafsir_vid_a = document.getElementById("tafsir_vid_a");
  tafsir_read_a = document.getElementById("tafsir_read_a");
  tafsir_text_p = document.getElementById("tafsir_text_p");

  tafsir_aud_a.href = source_aud;
  tafsir_vid_a.href = source_vid;
  tafsir_read_a.href = source_read;
  tafsir_text_p.innerHTML = text;
};

const set_data_q = (text, source_vid, source_aud, source_aud_telawa) => {
  tafsir_aud_a = document.getElementById("tafsir_aud_a");
  tafsir_vid_a = document.getElementById("tafsir_vid_a");
  tafsir_tel_a = document.getElementById("tafsir_tel_a");
  tafsir_text_p = document.getElementById("quran_text_p");
  tafsir_aud_a.href = source_aud;
  tafsir_vid_a.href = source_vid;
  tafsir_tel_a.href = source_aud_telawa;
  tafsir_text_p.innerHTML = text;
};
let prev_set_color = [];
const set_color = (id) => {
  for (let i = 0; i < prev_set_color.length; i++) {
    const element = document.getElementById(prev_set_color[i]);
    element.className = element.className.replace(" selc-active-had ", "selc-not-active-had");
  }
  prev_set_color = [];

  //     while(prev_set_color.length > 0 ){
  //         const element =prev_set_color.pop()
  //         element.className = element.className.replace(' selc-active-had ',"")
  // }

  const elm = document.getElementById(id);
  elm.className = elm.className + " selc-active-had ";

  prev_set_color.push(id);
};

function playAudio(source_id, audio_id) {
  var x = document.getElementById("#" + source_id);

  x.play();

  if (x.paused) {
    document.getElementById(audio_id).setAttribute("hidden", false);
  } else {
    x.pause();
    document.getElementById(audio_id).setAttribute("hidden", true);
  }
}
// do no thing
_ = () => { };

function scroll_to_div(id, img_src, item_file_url , type='audio/mpeg') {
  source_id = "main-audio" + id;
  let div = "a" + id;
  let audio = document.getElementById(source_id);
  var elm = document.getElementById(audio.id);
  var topPos = elm.offsetTop
  let menu_id = "side_menu_"+id;
  var selected_menu = document.getElementsByClassName("menu-active");
  if (selected_menu[0])
    selected_menu[0].classList.remove('menu-active');
  var me = document.getElementById(menu_id);
  if (me != null)
    me.classList.add("menu-active");
  scrollTo(document.getElementById(div), topPos-160, 600)
}

function play_pause_audio(id, img_src, item_file_url , type='audio/mpeg') {
  source_id = "main-audio" + id;
  img_id = "img" + id;
  let player = "player" + id;
  console.log("player", player);
  let menu_id = "side_menu_"+id;
  var selected_menu = document.getElementsByClassName("menu-active");
  if (selected_menu[0])
    selected_menu[0].classList.remove('menu-active');
  var me = document.getElementById(menu_id);
  if (me != null)
    me.classList.add("menu-active");
  let audio = document.getElementById(source_id);
  let img = document.getElementById(img_id);
  player = document.getElementById(player);

  if (audio.paused) {
    pause_all(img_src);
    if (!player.src) {
      player.src = item_file_url;
      // player.type = item_file_url;
      audio.load();
    }
    audio.play();
    img.src = img_src + "pause.jpg";
    played_audio.indexOf(id) === -1 ? played_audio.push(id) : _();
  } else {
    audio.pause();
    img.src = img_src + "play.jpg";
  }
}

function  scrollTop(element, to,  duration) {
    var start = element.scrollTop,
        change = to - start,
        currentTime = 0,
        increment = 20;
    var animateScroll = function(){
        currentTime += increment;
        var val = Math.easeInOutQuad(currentTime, start, change, duration);
        element.scrollTop = val;
        if(currentTime < duration) {
            setTimeout(animateScroll, increment);
        }
    };
    animateScroll();
}

Math.easeInOutQuad = function (t, b, c, d) {
	t /= d/2;
	if (t < 1) return c/2*t*t + b;
	t--;
	return -c/2 * (t*(t-2) - 1) + b;
};


const pause_all = (img_src) => {
  played_audio.forEach((id) => {
    source_id = "main-audio" + id;
    img_id = "img" + id;
    if (document.getElementById(source_id)) {
      var audio = document.getElementById(source_id);
      var img = document.getElementById(img_id);

      audio.pause();
      img.src = img_src + "play.jpg";
    }
  });
};
const played_audio = [];
const text_ids = [];
const text_quran = (text_id, show) => {
  const id = `text-read-${text_id}`;
  console.log($(`#${id}`));

  show ? $(`#${id}`).slideDown(500) : $(`#${id}`).slideUp(350);
};

const show_text_quran = (text_id) => {
  console.log("text_id", text_id);
  console.log("played_audio", played_audio);
  played_audio.forEach((el) => {
    text_quran(el, false);
  });
  const source_id = "main-audio" + text_id;
  let audio = document.getElementById(source_id);

  // const find = played_audio.find(el=>el===text_id)
  // console.log('find '+text_id)
  if (!audio.paused) {
    console.log("audio " + audio);

    text_quran(text_id, true);
  }
};

// When the user scrolls down 80px from the top of the document, resize the navbar's padding and the logo's font size
window.onscroll = function () {
  scrollFunction();
};

// const scoler_test = () => {
//   if ($(window).width() > 1024) {
//     new WOW().init();

//     function makeFixedHeader() {
//       var element = jQuery("#full_bar");
//       if (element.hasClass("makefixed")) return false;
//       element.addClass("makefixed");
//       element.children("div").addClass("animated bounceInDown");

//       // elms = document.getElementsByClassName("icon_nav_img");
//       // for (let index = 0; index < elms.length; index++) {
//       //   const el = elms[index];

//       //   // el.style.display  = " none";
//       //   el.style.visibility = " hidden";
//       //   el.style.opacity = 0;
//       //   el.style.maxHeight = "0";
//       // }

//       $('.icon_nav_img').slideUp(300);

//     }
//     function removeFixedHeader() {
//       var element = jQuery("#full_bar");
//       if (!element.hasClass("makefixed")) return false;
//       element.removeClass("makefixed");
//       element.children("div").removeClass("animated bounceInDown");
//       elms = document.getElementsByClassName("icon_nav_img");

//       // for (let index = 0; index < elms.length; index++) {
//       //   const el = elms[index];
//       //   // el.style.display  = " flex";
//       //   el.style.opacity = 1;
//       //   el.style.maxHeight = "100px";
//       //   el.style.visibility = " visible";
//       // }
//       // $('.icon_nav_img').show()
//       $('.icon_nav_img').slideDown(300);
//     }
//     // edit her 
//     height = jQuery(window).height()
//     let diff=120
//     if (height <=1200){
//       diff= 80
//     }
//     // end  edit  and use diff instend of 100 
//     jQuery(window).resize(function () {
//       var htop = $("#full_bar").height() + diff;
//       console.log(`htop ` + htop);
//       if (jQuery(window).scrollTop() >= htop) {
//         makeFixedHeader();
//       } else {
//         removeFixedHeader();
//       }
//     });
//     jQuery(window).scroll(function () {
//       var element = jQuery("#full_bar");

//       console.log(
//         `element.hasClass("makefixed") ` + element.hasClass("makefixed")
//       );

//       var htop = $("#full_bar").height() + diff;
//       console.log(`htop ` + htop);
//       if (jQuery(window).scrollTop() >= htop) {
//         makeFixedHeader();
//       } else {
//         removeFixedHeader();
//       }
//     });

//     $(".scrollup").click(function () {
//       // When arrow is clicked
//       $("body,html").animate(
//         {
//           scrollTop: 0, // Scroll to top of body
//         },
//         500
//       );
//     });
//   } else {
//   }
// };

const scoler_test = () => {
  if ($(window).width() > 1024) {
    new WOW().init();

    function makeFixedHeader() {
      var element = jQuery("#full_bar");
      if (element.hasClass("makefixed")) return false;
      element.addClass("makefixed");
      element.children("div").addClass("animated bounceInDown");


      $('.icon_nav_img').slideUp(300);

    }
    function removeFixedHeader() {
      var element = jQuery("#full_bar");
      if (!element.hasClass("makefixed")) return false;
      element.removeClass("makefixed");
      element.children("div").removeClass("animated bounceInDown");
      elms = document.getElementsByClassName("icon_nav_img");


      $('.icon_nav_img').slideDown(300);
    }
    // edit her 
    height = jQuery(window).height()
    let diff = 120
    if (height <= 1200) {
      diff = 80
    }
    // end  edit  and use diff instend of 100 
    jQuery(window).resize(function () {
      var htop = $("#full_bar").height() + diff;
      console.log(`htop ` + htop);
      if (jQuery(window).scrollTop() >= htop) {
        makeFixedHeader();
      } else {
        removeFixedHeader();
      }
    });
    jQuery(window).scroll(function () {
      var element = jQuery("#full_bar");

      console.log(
        `element.hasClass("makefixed") ` + element.hasClass("makefixed")
      );

      var htop = $("#full_bar").height() + diff;
      console.log(`htop ` + htop);
      if (jQuery(window).scrollTop() >= htop) {
        makeFixedHeader();
      } else {
        removeFixedHeader();
      }
    });

    $(".scrollup").click(function () {
      // When arrow is clicked
      $("body,html").animate(
        {
          scrollTop: 0, // Scroll to top of body
        },
        500
      );
    });
  } else {
  }
};

function scrollFunction() {
  scoler_test();
  return;

  const base_color = "#00000066";
  const move_color = "#00000094";
  document.getElementById("main_bar_in_header").style.zIndex = 2000;
  const body = document.body,
    html = document.documentElement;

  const height = Math.max(
    body.scrollHeight,
    body.offsetHeight,
    html.clientHeight,
    html.scrollHeight,
    html.offsetHeight
  );

  // if (height >= 1100)
  let scroll_on = height >= 1100 ? 120 : 360;
  console.log("height,scroll_on", height, scroll_on);
  let margin = scroll_on - 80;
  if (
    document.body.scrollTop > scroll_on ||
    document.documentElement.scrollTop > scroll_on
  ) {
    document.getElementById("content-header").style.position = "fixed";
    document.getElementById("content-header").style.zIndex = 20001;

    document.getElementById("main_bar_in_header").style.position = "fixed";
    const content_header_h =
      document.getElementById("content-header").offsetHeight;

    document.getElementById("main_bar_in_header").style.top =
      content_header_h + "px";

    elms = document.getElementsByClassName("icon_nav_img");
    for (let index = 0; index < elms.length; index++) {
      const el = elms[index];

      // el.style.display  = " none";
      el.style.visibility = " hidden";
      el.style.opacity = 0;
      el.style.maxHeight = "0";
    }
  } else if (
    document.body.scrollTop > margin || document.documentElement.scrollTop > margin
  ) {
  } else {
    document.getElementById("content-header").style.position = "static";
    document.getElementById("content-header").style.zIndex = 10;

    document.getElementById("main_bar_in_header").style.position = " inherit";

    const content_header_h =
      document.getElementById("content-header").offsetHeight;
    document.getElementById("main_bar_in_header").style.top =
      content_header_h + "px";

    elms = document.getElementsByClassName("icon_nav_img");
    for (let index = 0; index < elms.length; index++) {
      const el = elms[index];
      // el.style.display  = " flex";
      el.style.opacity = 1;
      el.style.maxHeight = "100px";
      el.style.visibility = " visible";
    }
  }
}

// content_header_height= "",

// new ResizeSensor(jQuery('#content-header'), function(){
//     console.log('content dimension changed');
//     content_header_height = document.getElementById('myDiv').offsetHeight;

// });

scrollFunction();
// .content .header
//  position: fixed;
// z-index: 1;

// get prayer time

function httpGet(theUrl) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", theUrl, false); // false for synchronous request
  xmlHttp.send(null);
  return xmlHttp.responseText;
}

let prayer_data = {};

const get_prayer_by_city = (url, tawqit, city, path) => {
  const if_null_and_msg = (val, pray_name) => {
    if (!val || val == "-") return "غير متوفر";

    if (pray_name == "شروق")
      return "الشروق" + "<span>" + val + "</span>  " + " بتوقيت " + tawqit;
    else
      return (
        "صلاة   " +
        pray_name +
        "<span>" +
        val +
        "</span>  " +
        " بتوقيت " +
        tawqit
      );
  };

  let obj;
  console.log(prayer_data);
  if (prayer_data[city]) {
    obj = prayer_data[city];
  } else {
    result = httpGet(url);

    obj = JSON.parse(result);
    console.log(obj);
    if (obj.code == 200) {
      obj = obj.results.datetime[0].times;
      prayer_data[city] = obj;
    }
  }
  // const result = httpGet(url)

  // const obj = JSON.parse(result)

  // {"mecca": {"Fajr": "5:32", "Sunrise": "6:44", "Dhuhr": "12:34", "Asr": "15:54", "Maghrib": "18:36", "Isha": null}}
  // document.getElementById("prayer_Fajr").innerHTML =if_null_and_msg( obj.Fajr ,'الفجر');
  // document.getElementById("prayer_Sunrise").innerHTML = if_null_and_msg (obj.Sunrise ,'الشروق')
  // document.getElementById("prayer_Dhuhr").innerHTML = if_null_and_msg (obj.Dhuhr ,'الظهر')

  // document.getElementById("prayer_Asr").innerHTML =if_null_and_msg ( obj.Asr ,'العصر')
  // document.getElementById("prayer_Maghrib").innerHTML = if_null_and_msg (obj.Maghrib ,'المغرب')
  // document.getElementById("prayer_Isha").innerHTML = if_null_and_msg (obj.Isha ,'العشاء')
  const show = (id, elm) => {
    $("#" + id)
      .parent()
      .fadeOut(300, () => {
        $("#" + id).html(elm);
        $("#" + id)
          .parent()
          .fadeIn("slow");
      });
  };

  show("prayer_Fajr", if_null_and_msg(obj.Fajr, "الفجر"));
  show("prayer_Sunrise", if_null_and_msg(obj.Sunrise, "شروق"));
  show("prayer_Dhuhr", if_null_and_msg(obj.Dhuhr, "الظهر"));
  show("prayer_Asr", if_null_and_msg(obj.Asr, "العصر"));
  show("prayer_Maghrib", if_null_and_msg(obj.Maghrib, "المغرب"));
  show("prayer_Isha", if_null_and_msg(obj.Isha, "العشاء"));

  const city_list_id = ["toronto", "mecca", "alex", "abu-dhabi"];

  for (let index = 0; index < city_list_id.length; index++) {
    const elm = city_list_id[index];
    let div_id = elm + "-city";
    let img_id = elm + "-img";

    let div = document.getElementById(div_id);
    let img = document.getElementById(img_id);
    console.log("elm,city", elm, city);
    if (elm.includes(city)) {
      // div.style.backgroundColor="var(--active-color)"
      img.src = path + "/active/" + elm + ".png";
      div.classList.add("active");
    } else {
      img.src = path + "/inactive/" + elm + ".png";
      div.classList.remove("active");
      //.backgroundColor="white"
    }
  }
};
