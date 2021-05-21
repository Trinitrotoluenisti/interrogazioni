let colors = ["red", "green", "yellow", "blue", "purple", "aqua", "orange"];


let lists = document.getElementsByClassName("list");

for (var i = 0; i < lists.length; i++) {
    lists[i].style.backgroundColor = "var(--" + colors[i % colors.length] + ")";
};
