
    // User entering webpage will be locked out of scrolling until explore more button is pressed
    // When Explore More/#scroll-enable is pressed User will be automatically scrolled to #down id

window.onload = function() {
  // disable scrolling on page load
  getNotification();
  document.documentElement.style.overflow = 'hidden';
  document.body.scroll = "no";
  var scroll_element = document.getElementById("down");

  // enable scrolling on link click
  document.getElementById('enable-scroll').addEventListener('click', function() {
    document.documentElement.style.overflow = 'auto';
    document.body.scroll = "yes";
    scroll_element.scrollIntoView({
      behavior: "smooth",
      block: "start",
      inline: "nearest"
    });
  });
  window.onscroll=calcScrollValue;
  window.onload=calcScrollValue;
};

const context = document.getElementById('context-anim');

context.addEventListener('animationend', () => {
  context.classList.add('reappear');
});

// Slideshow of images for Zodiac Series | First Image must always be the same as html displayed image
const images = ['/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/main.webp',
                '/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/img_1.webp',
                '/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/img_2.webp',
                '/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/img_3.webp',
                '/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/img_4.webp',
                '/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/img_5.webp',
                '/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/img_6.webp',
                '/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/img_7.webp',
                '/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/img_8.webp',
                '/static/img/POPtrade/WHAT_I_USED/ZodiacSeries/img_9.webp'];

let counter = 0;

// loads #img-js & #slider-bar into imageElement & barElement
const imageElement = document.getElementById("img-js");
const barElement = document.getElementById("slider-bar");
barElement.style.width = "0%";

// Increment along array and display to Elements + Increment Slider bar
function changeImage() {
    counter++;
    if (counter >= images.length) {
    counter = 0;
    }
    const nextImage = images[counter];
    imageElement.setAttribute("src", nextImage);
    barElement.style.width =  ((counter+1) / images.length) * imageElement.clientWidth  + "px";

}

let intervalId;

// Detects Mouse Hover
imageElement.addEventListener("mouseover", function() {
  intervalId = setInterval(changeImage, 1000);
  barElement.style.display = "block";
});

// Detects Mouse Exit Hover
imageElement.addEventListener("mouseout", function() {
  clearInterval(intervalId);
  imageElement.setAttribute("src", images[0]);
  barElement.style.display = "none";
  barElement.style.width = "0%";
});

// function postFunction(){
//   var userUrl = document.getElementById("userUrl");
//   userUrl.href = "/auth/user/{{ g.user['id'] }}";
// }

// function getNotification(){
//   fetch("/notification/getNotification",{
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json'
//       },
//       body:JSON.stringify({
//           "user_id": "{{g.user['id']}}"
//       })
//   })
//   // then(alert(Response.text))
//   .then((response)=>response.text())
//   .then((text)=>{
//       document.getElementById("notification-link").innerHTML = text;
//   })
// }


//=====================    Using Fade | NOT WORKING DO NOT USE  ==========================

//    function changeImage(){
//        counter++;
//        if(counter >= images.length){
//            counter = 0;
//        }
//        const nextImage = images[counter];
//        const tempImage = document.createElement("img");
//        tempImage.src = nextImage;
//        tempImage.style.opacity = "0";
//        tempImage.addEventListener("load", function(){
//            imageElement.style.opacity = "0";
//            imageElement.setAttribute("src", nextImage);
//            imageElement.addEventListener("transitionend", function(){
//                imageElement.style.opacity = "1";
//            });
//            barElement.style.width = ((counter+1) / images.length) * 100 + "%";
//        });
//    }
//
//    let intervalId;
//
//    imageElement.addEventListener("mouseover", function() {
//      intervalId = setInterval(changeImage, 1000);
//      barElement.style.display = "block";
//    });
//
//    imageElement.addEventListener("mouseout", function(){
//        clearInterval(intervalId);
//        imageElement.setAttribute("src", images[0]);
//        imageElement.style.opacity = "1";
//        barElement.style.display = "none";
//        barElement.style.width = "0%";
//    });

// ============= Without the slider bar - just slideshow of images ==============

//    let counter = 0;
//
//    const imageElement = document.getElementById("img-js");
//
//    function changeImage() {
//      counter++;
//      if (counter >= images.length) {
//        counter = 0;
//      }
//      const nextImage = images[counter];
//      imageElement.setAttribute("src", nextImage);
//    }
//
//    let intervalId;
//
//    imageElement.addEventListener("mouseover", function() {
//      intervalId = setInterval(changeImage, 1000);
//    });
//
//    imageElement.addEventListener("mouseout", function() {
//      clearInterval(intervalId);
//      imageElement.setAttribute("src", images[0]);
//    });
