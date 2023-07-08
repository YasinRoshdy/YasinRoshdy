const change_daily_taps = (evt, index) => {
    tab_name="daily_tap_"+index
    img_src="img_src_"+index

    for (let i =1; i < 5; i++) {
        _id = "img_src_"+i
        
        
        img = document.getElementById(_id)
        src = img.src
        
        
        if (i==index) {
            img.src =  src.replace('in','active')
            
        }else 
        img.src =  src.replace('active','in')
    }
    let i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("daily_tap");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tab_name).style.display = "block";
    evt.currentTarget.className += " active";
};

document.getElementById("defaultOpen").click();