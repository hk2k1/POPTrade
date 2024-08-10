let text = document.getElementById("text");
let left = document.getElementById("chara-left");
let dimoo = document.getElementById("chara-top");

window.addEventListener("scroll", ()=>{
  let value = window.scrollY;
  if ((value*2.5)  < 2000){
    text.style.marginTop = value * 2.5 + "px";
  }
  else{
    text.style.marginTop = 0 + "px";
  }
  left.style.left = value * -1.5 + "px";
  dimoo.style.top = value * -1.5 + "px";

});
