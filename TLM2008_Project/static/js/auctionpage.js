     // Toggle Heart to Red
    function toggleHeartColor() {
        const heart = document.getElementById("heart");
        if (heart.classList.contains("red")) {
          heart.classList.remove("red");
        } else {
          heart.classList.add("red");
        }
    }
    
    function toggleHeartColor(isFavourite) {
      const heart = document.getElementById("heart");
      console.log("status:");
      console.log(isFavourite);
      if(isFavourite == true){
        heart.classList.add("red");
      }
      else if(isFavourite == 1) {
        heart.classList.add("red");
      }
      else if(isFavourite == false){
        heart.classList.remove("red");
      }
      else if(isFavourite == 0) {
        heart.classList.remove("red");
      }
      // if (heart.classList.contains("red")) {
      //   heart.classList.remove("red");
      // } else {
      //   heart.classList.add("red");
      // }
    }
    
    // Toggle Star to Orange
    function toggleStarColor() {
      const star = document.getElementById("star");
      if (star.classList.contains("orange")) {
        star.classList.remove("orange");
      } else {
        star.classList.add("orange");
      }
    }
    
    
    function showImage(imageUrl) {
      var largeImage = document.getElementById("large-image");
      largeImage.src = imageUrl;
    }
    
    function updatePrice(price) {
      document.getElementById('item-price').innerHTML = price;
    }
    
    function slideProducts(direction) {
      const container = document.querySelector('.products-list');
      const scrollDistance = 400;
      
      if (direction === 'left') {
        container.scroll({
          left: container.scrollLeft - scrollDistance,
          behavior: 'smooth',
          block: 'nearest'
        });
      } else if (direction === 'right') {
        container.scroll({
          left: container.scrollLeft + scrollDistance,
          behavior: 'smooth',
          block: 'nearest'
        });
      }
    }
    
    $(window).scroll(function() {
      var scrollTop = $(this).scrollTop();
      var triggerPosition = $(window).height() / 2.5;
      if (scrollTop > triggerPosition) {
          // Trigger the animation
          $('.bottom-container').css('opacity', 1);
        }
        else{
          $('.bottom-container').css('opacity', 0);
        }
      });
    
    $(document).ready(function() {
        $('.nav-img').click(function() {
            $('.nav-img').removeClass('selected');
            $(this).addClass('selected');
        });
    });

    console.log(window.location.href);
    const stringArray = window.location.href.split("/");
    let itemID = stringArray[stringArray.length - 2];
    console.log(itemID);
    document.getElementById("bidItem").value = itemID;
    document.getElementById("biddingForm").action = "/auction/auctionItem/bid/" + itemID;

    //document.getElementById("biddingForm").action = "/auction/auctionItem/bid/";
    function alertFunction(){
        alert("Bid submitted!")
    }


function toggleCollapse2() {
  var content = document.getElementById("itemDesc");
  var header = document.getElementById("desc-head");
  
  if (content.style.display === "none") {
    content.style.display = "block";
    header.classList.remove("arrow-left");
    header.classList.add("arrow-down");
  } else {
    content.style.display = "none";
    header.classList.remove("arrow-down");
    header.classList.add("arrow-left");
  }
}

function toggleCollapse3() {
  var content = document.getElementById("termsCondi");
  var header = document.getElementById("terms-head");
  
  if (content.style.display === "none") {
    content.style.display = "block";
    header.classList.remove("arrow-left");
    header.classList.add("arrow-down");
  } else {
    content.style.display = "none";
    header.classList.remove("arrow-down");
    header.classList.add("arrow-left");
  }
}


function favItem(){

  fetch('/auction/auctionItem/favItem/', {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'item_id': "random",
      'user_id': "random",
    })
  })
  // .then(function(data){
  //   alert('Item added to favourites!')
  // })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    toggleHeartColor(data.status);
  })
}