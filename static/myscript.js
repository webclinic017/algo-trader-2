
const currentLocation = location.href;
const menuItem = document.querySelectorAll('a');
const menuLength = menuItem.length;
for (let i=0; i<menuLength; i++){
	if(menuItem[i].href === currentLocation){
		menuItem[i].className = "active"
	}
}




//function myFunction() {
//  x=document.getElementById("title").innerHTML;
//  y=document.getElementById("home");
//  document.getElementById("test").innerHTML=x.classname
//}
