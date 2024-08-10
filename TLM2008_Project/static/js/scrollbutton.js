// javacsript topbutton code{

    
//     }

function calcScrollValue() {
    let scrollProgress = document.getElementById("progress");
    // let progressValue = document.getElementById("progress-value");
    let pos = document.documentElement.scrollTop;
    console.log(pos);
    let calcHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    let scrollValue = Math.round((pos * 100) / calcHeight);

    if (pos > 1500) {
        if(!scrollProgress.classList.contains("btnEntrance")){
            scrollProgress.classList.remove("btnExit");
            scrollProgress.classList.add("btnEntrance");
            scrollProgress.style.display = "grid";
            console.log("JOE MAMA DID IT");
        }
    }

    else {
        // scrollProgress.classList.add("btnExit");
        if(scrollProgress.classList.contains("btnEntrance")){
            scrollProgress.classList.remove("btnEntrance");
            scrollProgress.classList.add("btnExit");
            setTimeout(function(){
                scrollProgress.style.display = "none";
            }, 250);
        }
        
    }

    scrollProgress.addEventListener("click", () => {
        // if(scrollProgress.classList.contains("btnEntrance")){
        //     scrollProgress.classList.remove("btnEntrance");
        //     scrollProgress.classList.add("btnExit");
        //     setTimeout(function(){
        //         document.documentElement.scrollTop = 0;
        //         scrollProgress.style.display = "none";
        //     }, 250);
        // }
        setTimeout(function(){
            document.documentElement.scrollTop = 0;
            // scrollProgress.style.display = "none";
        }, 250);
    });

    // scrollProgress.style.backgroundImage = "conic-gradient (#03cc65 {$scrollValue}%, #d7d7d7 {$scrollValue}%)";
    scrollProgress.style.background = "conic-gradient(#ffdada " + scrollValue+"%"+ ", #d7d7d7 " + scrollValue+"%"+ ")";
    console.log(scrollValue);
}


function isElementInViewport(el) {
    var rect = el.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }
  
  function handleScroll() {
    var titles = document.querySelectorAll('.title');
    var firstTitleInView = null;
    for (var i = 0; i < titles.length; i++) {
      var title = titles[i];
      if (isElementInViewport(title)) {
        firstTitleInView = title;
        break;
      }
    }
    for (var i = 0; i < titles.length; i++) {
      var title = titles[i];
      if (title === firstTitleInView) {
        title.classList.add('expanded');
      } else {
        title.classList.remove('expanded');
      }
    }
  }
  
  window.addEventListener('scroll', handleScroll);
  
// These windows doms are in sldier.js file
// window.onscroll=calcScrollValue;
// window.onload=calcScrollValue;