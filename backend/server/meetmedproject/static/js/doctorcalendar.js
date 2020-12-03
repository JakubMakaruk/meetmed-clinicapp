document.getElementById("close-add").addEventListener("click", function(){
    document.getElementsByClassName("popup-add")[0].classList.remove("active");
    document.getElementById("popup-remove-background").style.display = "none";
});

document.getElementById("close-remove").addEventListener("click", function(){
    document.getElementsByClassName("popup-remove")[0].classList.remove("active");
    document.getElementById("popup-remove-background").style.display = "none";
});
