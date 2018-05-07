<!DOCTYPE HTML>
<%
    //String path = request.getContextPath();
	String normalPath=request.getScheme()+"://"+request.getServerName();
   // String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
    //String menuPath=request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+"/website/";
%>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FPS Estimator - Estimation</title>
<link rel="shortcut icon" href="../resources/icon/favicon.ico" />
<!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
-->
 <link rel="stylesheet" href="../resources/css/bootstrap.min.css">
  <link rel="stylesheet" href="../resources/css/open-iconic-bootstrap.min.css">
<!--   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"> --> 

 <script src="../resources/js/jquery.min.js"></script>
   <script src="../resources/js/tether.min.js"></script>
  <script src="../resources/js/bootstrap.min.js"></script>
   <link rel="stylesheet" href="../resources/css/jquery-ui.min.css">
    <script src="../resources/js/jquery-ui.min.js"></script>
  <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.17.0/jquery.validate.min.js"></script>  -->
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-118399528-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-118399528-1');
</script>

<style>
#loader-wrapper{
	-webkit-transition: all 0.3s ease-out 1s ; 
	transition: all 0.3s ease-out 1s ;
	position:fixed;
	width:100%;
	height:100vh;
	top:0;
	left:0;
	z-index:1099;
}
#loader-wrapper .loader-section {
    position: fixed;
    top: 0;
    width: 51%;
    height: 100%;
    background: #222222;
    z-index: 1100;
	-webkit-transition: all 0.7s cubic-bezier(0.645, 0.045, 0.355, 1.000); 
	transition: all 0.7s cubic-bezier(0.645, 0.045, 0.355, 1.000);
}
#loader-wrapper .loader-section.section-left {
    left: 0;
}
#loader-wrapper .loader-section.section-right {
    right: 0;
}
#loader {
    z-index: 1101;
	border: 8px solid #3a3535;
    border-top: 8px solid #cecece;
    border-radius: 50%;
    width: 120px;
    height: 120px;
	margin: -60px 0 0 -60px;
	top:50%;
	left:50%;
	position:relative;
	opacity:1;
    animation: spin 2s linear infinite;
	transition: all 0.3s ease-in 1.3s;
	-webkit-transition: all 0.3s ease-in 1.3s; 
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.loaded #loader-wrapper .loader-section.section-left {
    -webkit-transform: translateX(-100%);  /* Chrome, Opera 15+, Safari 3.1+ */
    -ms-transform: translateX(-100%);  /* IE 9 */
    transform: translateX(-100%);  /* Firefox 16+, IE 10+, Opera */
}
.loaded #loader-wrapper .loader-section.section-right {
    -webkit-transform: translateX(100%);  /* Chrome, Opera 15+, Safari 3.1+ */
    -ms-transform: translateX(100%);  /* IE 9 */
    transform: translateX(100%);  /* Firefox 16+, IE 10+, Opera */
}
.loaded #loader {
	opacity:0;
	transition: all 0.3s ease-in;
	-webkit-transition: all 0.3s ease-in;
}
.loaded #loader-wrapper {
	width:0px;
}
.loaded #loader-wrapper .loader-section{
	-webkit-transition: all 0.7s cubic-bezier(0.645, 0.045, 0.355, 1.000) 0.3s; 
	transition: all 0.7s cubic-bezier(0.645, 0.045, 0.355, 1.000) 0.3s;
}
body{

  background: linear-gradient(to right, rgba(232,231,232,0), rgba(232,231,232,1));
}
header{
    position: -webkit-sticky; /* Safari */
    position: sticky;
/*background-color:#918E8C;*/
}
footer{
background-color:#142D42;
padding-bottom:10px;
}
header .row{
	position:relative;
	background-color:#142D42;
}
img.responsive{
width:100%;
height:auto;
}
a{
cursor:pointer !important;
color:#007bff !important;
}
a:hover{
color:blue !important;
}
a.unchecked{
color:black !important;
pointer-events: none;
}
.videoWrapper {
	position: relative;
	padding-bottom: 56.25%; /* 16:9 */
	padding-top: 25px;
	height: 0;
}
.videoWrapper iframe {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
}
div.nav-wrapper{
background:linear-gradient(to bottom, #152F45, #193954);
}
@media (min-width:768px){
div.nav-wrapper{
position:absolute;
bottom:0px;
right:0px;
}
}
@media (max-width:576px){
.autoDisableForMobile{
margin-top:10px;
}
}
@media (min-width:576px){
.autoDisableForMobile{
display:none;
}
}
/*
nav{
position:absolute;
bottom:0px;
}
*/

nav ul{
padding:0px 0px;
margin-bottom: 5px;

}
nav ul li{
margin-right:10px !important;
min-height:30px;
background-color:transparent !important;
}
nav ul li a{
color:white !important;
}
nav ul li:hover a{
color:#DCDAFF !important;
}
span.main-nav{
font-size:2.5rem;
}

.main-select-col > div{
margin-top:30px;
padding:10px 5px;
}

.main-select-col > div > div{
text-align:center;
}

.main-select-col > div > div ul{
text-align:center;
}
.main-select-col > div > div li{
display:inline;
}
.main-select-col > :first-child{
margin-top:0px;
}
.another-select-col > div{
margin-top:8px;
display:flex;
}

.another-select-col{

}
.center{
    margin: auto;
    width: 50%;
}
button{
    margin: 0 auto;
}
div.dropdown-list{
	background-color:#d7d7d7;
	padding-top:10px;
}

		#cpu-model-name .list-group{
	max-height:20rem;
		overflow-y:auto;
	}
			#gpu-model-name .list-group{
	max-height:20rem;
		overflow-y:auto;
	}
				#game-name .list-group{
	max-height:20rem;
		overflow-y:auto;
	}
div.dropdown-list > p{
margin-bottom:10px;
}
div.dropdown-list > input{
width:90%;
margin-left:5%;
margin-bottom:10px;
}
.another-select-col-label{
	width:65%;
	padding-left:5%;
	text-align:left;
}
button.select-btn{
width:100%;
display:flex;
white-space:normal !important;
word-wrap: break-word;
}
section .carousel-inner{
width:80%;
margin-left:10%;
margin-bottom:50px;
}
header .wrapper{
width:90%;
margin:0px 5%;
}
section .wrapper{
width:90%;
margin-left:5%;
padding-top:25px;
padding-bottom:15px;
}
footer .wrapper{
width:90%;
margin-left:5%;
display:flex;
justify-content: space-between;
}
.resolution-input div{
padding:0px 0px;
}
span.selected{

    text-decoration: underline;
    -webkit-text-decoration-color: red; /* Safari */    
    text-decoration-color: red;
	text-decoration-style:wavy;

}
#display-column{
text-align:center;
padding:2px 4px 2px 4px;
}
#display-column p,#display-column span{
width:100%;
}
span.references{
color:#707070;
font-size:0.8rem;}
#main-content{
}
#main-content h1,#main-content h2,#main-content h3,#main-content p{
text-align:center;
margin-bottom:0.3rem;
}
#main-content h1{
color:#142D42;
}
#main-content h2,#main-content h3,#main-content p{
color:#1B3D59;
}
#main-content p.references{
color:grey;
font-size:0.8rem;}
#other-content .row .carousel{
    border: 2px solid grey;
    border-radius: 8px;
    background-color:#DBD8E0;
}
#other-content h1{
color:#142D42;
}
#other-content h2,#other-content h3,#other-content p{
color:#1B3D59;
}
footer p{
color:white !important;
}
.description h4{
 text-align:center;
}
@media (min-width:768px){
.col-md-offset-2{
margin-left:16.6%;
}

}
@media (min-width:960px){
.col-lg-offset-1-2{
margin-left:4%;
}

}
@media (min-width:1140px){
.col-xl-offset-1{
margin-left:8%;
}

}
.selection{
background-color:#969696;
}
.btn-primary{
background-color: #00438C;
border-color: #00336B;
border-style: solid;
    border-width: 2px;
}
#guide h1{
margin:0px 0px;
}
#guide p{
margin: 0px 0px;
color:grey;
font-size=0.8rem;
}
@media (max-width:2000px){
.partial-visible{
display:none;
}
}
.loaderContainer{
width:80%;
margin-left:10%;
position:relative;
}
.loaderInner{
    width: 100%;
    padding-top: 100%; /* 1:1 Aspect Ratio */
    position: relative; /* If you want text inside of it */
}
.loader {
    border: 16px solid #f3f3f3; /* Light grey */
    border-top: 16px solid #3498db; /* Blue */
    border-radius: 50%;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
#select-game .invisible-icon{
display:none;
}

@media (max-width:576px){
.col-offset-2{
margin-left:16.66666%;
}
.col-offset-2-1-2{
margin-left:20.8333333%;
}
#select-cpu span.glyphicon, #select-cpu span.oi{
display:none;}
#select-gpu span.glyphicon, #select-gpu span.oi{
display:none;}
#select-game span.glyphicon, #select-game span.oi{
display:none;}

}
.select-game{
margin-bottom:30px;
}
.inner-addon { 
    position: relative;

    margin-bottom:10px;
}

/* style icon */
.inner-addon .glyphicon,.inner-addon .oi  {
  position: absolute;
  padding: 10px;
pointer-events: fill;
}

/* align icon */
.left-addon .glyphicon, .left-addon .oi  { left:  0px;}
.right-addon .glyphicon, .right-addon .oi { right: 0px;}

/* add padding  */
.left-addon input  { padding-left:  30px; }
.right-addon input { padding-right: 30px; }
.oi{
vertical-align: middle;
}
@media (max-width:576px){
.col-md-6,.col-md-4,.col-md-12{
padding:0px 0px;
margin:0px 0px;
}
}
.settingRemark{
color:black;text-shadow: 2px 2px 8px #707070;
}
button.unchecked{
color:black !important;
pointer-events: none;
}
.setting-remark{
font-size:0.3rem;}
</style>
<script>
/*
var gameList=[];
 $.ajax({
        type: "GET",
        //would be change later
        url: "http://localhost:8081/fpsestimator/Game",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            console.log(response);
            i = 0;
            if (response!=null&&response.length !=0) {
                while (response[i] != null) {	
                	var temp = {label:response[i].Name, value:response[i].Name};
                	gameList.push(temp);
                    i++;
                };
                $('#game').autocomplete({
                	source:gameList,
                	select: function( event, ui ) {
                			event.preventDefault();
	                		$(this).val(ui.item.label);
	                		//getCustomerDetail(ui.item.value);
	                		console.log("You have selected\nLabel:"+ui.item.label+"\nValue:"+ui.item.value);
                		}
                    });
            	}
        },
        failure: function (response) {
            console.log("Unable to connect Database");
        },
        error: function (response) {
        	console.log("Unable to connect Database");
        }
    });
	*/
	var cpuList=[];
	var presentCPUList=[];
	var presentCPU="";
		var gpuList=[];
		var presentGPUList=[];
	var presentGPU="";
	var gameList=[];
	/*var checkingTimeOut;
	function checkCPUandGPU(preset) {
		if(preset==false){
			alert("Unable to get all CPU and GPU Data\nOK for continue anyway");
			$('body').addClass('loaded');
			return false;
		}
		if(cpuList==null || gpuList==null ||cpuList[0]==null|| cpuList[1]==null||gpuList[0]==null||gpuList[1]==null) {
			return false;
		}
		else{
			$('body').addClass('loaded');
			clearTimeout(checkingTimeOut);
			return true;
		}
	}
	*/
	function updateGameList(str,isFirst){
		var cnt=0
		$('#game-name ul').html("");
		for (var i=0;i<gameList.length;i++){
			if ((gameList[i]+"").toUpperCase().includes(str.toUpperCase())){
				var newli="<li class='list-group-item'><a>"+gameList[i]+"</a></li>";
				newli=$(newli)
				newli.click(function(){
					var gamename=$(this).text()+"";
					console.log('Selected '+gamename);
					var newElement="<span class='selected'>"+gamename+"</span>";
					$('#select-game p.col-sm-10').html(newElement);
					$('#game-name').collapse("hide");
				});
				$('#game-name ul').append(newli);
			

				cnt+=1;
			}
			if(isFirst==false && cnt>=7) break;
		
		}
		if (cnt==0){
			var newli="<li class='list-group-item'>Nothing Found</li>";
			$('#game-name ul').append(newli);
		}	
	}
	$(document ).ready(function() {
		var cpuBrand="Intel";
		$.ajax({
			type: "GET",
			//would be change later
			url: "../CPU/"+cpuBrand,
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function (response) {
				console.log(response);
				var i = 0;
				if (response!=null&&response.length !=0) {
					if (cpuList==null||cpuList[0]==null||cpuList[0].length==0){
						var tempResponseList=[];
						while (response[i] != null) {	
							var temp = response[i].Name+"";
							tempResponseList.push(temp);
							i++;
						};
						cpuList[0]=tempResponseList;
					}
				}
				//checkCPUandGPU(true);
				$('#cpu-brand .list-group-item:nth-child(1) .oi').css('display','none');
				$('#cpu-brand .list-group-item:nth-child(1) a').removeClass('unchecked');
			},
			failure: function (response) {
				console.log("Unable to connect Database");
			},
			error: function (response) {
				console.log("Unable to connect Database");
			}
		});
		cpuBrand="AMD";
		$.ajax({
			type: "GET",
			//would be change later

			url: "../CPU/"+cpuBrand,
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function (response) {
				console.log(response);
				var i = 0;
				if (response!=null&&response.length !=0) {
					if (cpuList==null||cpuList[1]==null||cpuList[1].length==0){
						var tempResponseList=[];
						while (response[i] != null) {	
							var temp = response[i].Name+"";
							tempResponseList.push(temp);
							i++;
						};
						cpuList[1]=tempResponseList;
					}
				}
				//checkCPUandGPU(true);
				$('#cpu-brand .list-group-item:nth-child(2) .oi').css('display','none');
				$('#cpu-brand .list-group-item:nth-child(2) a').removeClass('unchecked');
			},
			failure: function (response) {
				console.log("Unable to connect Database");
			},
			error: function (response) {
				console.log("Unable to connect Database");
			}
		});
		var gpuBrand="Nvidia";
		$.ajax({
			type: "GET",
			//would be change later
			url: "../GPU/"+gpuBrand,
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function (response) {
				console.log(response);
				var i = 0;
				if (response!=null&&response.length !=0) {
					if (gpuList==null||gpuList[0]==null||gpuList[0].length==0){
						var tempResponseList=[];
						while (response[i] != null) {	
							var temp = response[i].Name+"";
							tempResponseList.push(temp);
							i++;
						};
						gpuList[0]=tempResponseList;
					}
				}
				//checkCPUandGPU(true);
				$('#gpu-brand .list-group-item:nth-child(1) .oi').css('display','none');
				$('#gpu-brand .list-group-item:nth-child(1) a').removeClass('unchecked');
			},
			failure: function (response) {
				console.log("Unable to connect Database");
			},
			error: function (response) {
				console.log("Unable to connect Database");
			}
		});
		var gpuBrand="AMD";
		$.ajax({
			type: "GET",
			//would be change later
			url: "../GPU/"+gpuBrand,
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function (response) {
				console.log(response);
				var i = 0;
				if (response!=null&&response.length !=0) {
					if (gpuList==null||gpuList[1]==null||gpuList[1].length==0){
						var tempResponseList=[];
						while (response[i] != null) {	
							var temp = response[i].Name+"";
							tempResponseList.push(temp);
							i++;
						};
						gpuList[1]=tempResponseList;
					}
				}
				//checkCPUandGPU(true);
				$('#gpu-brand .list-group-item:nth-child(2) .oi').css('display','none');
				$('#gpu-brand .list-group-item:nth-child(2) a').removeClass('unchecked');
			},
			failure: function (response) {
				console.log("Unable to connect Database");
			},
			error: function (response) {
				console.log("Unable to connect Database");
			}
		});
		//$('#select-game button .oi').css("display","none");
		//$('#select-game button .loading-icon').css("display","block");
		$.ajax({
			type: "GET",
			//would be change later
			url: "../Game",
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function (response) {
				console.log(response);
				var i = 0;
				if (response!=null&&response.length !=0) {
					if (gameList.length==0){
						while (response[i] != null) {	
							var temp = response[i].Name+"";
							gameList.push(temp);
							i++;
						};
					}
				}
				//checkCPUandGPU(true);
				$('#select-game button .invisible-icon').removeClass("invisible-icon");
				$('#select-game button .loading-icon').css("display","none");

				$('#select-game button').removeClass('unchecked');
				//$('#game').trigger('change');
				updateGameList("",true);
				
			},
			failure: function (response) {
				console.log("Unable to connect Database");
			},
			error: function (response) {
				console.log("Unable to connect Database");
			}
		});
		//prepare model
		$.ajax({
			type: "GET",
			//would be change later

				url: "<%=normalPath%>:5000/predict",
				contentType: "application/json; charset=utf-8",
				dataType: "json",
			dataType: "json",
			success: function (response) {
				console.log(response);

			},
			failure: function (response) {
				console.log(response);
			//	var response=response.responseText;
				//response=response.replace(/\"/g,"");
				$('#display-column').html("<span style='color:red'>Unable to call service</span>");
			},
			error: function (response) {
				console.log(response);
				$('#display-column').html("<span style='color:red'>Unable to call service</span>");
			}
		});
		//prepare model
		//checkingTimeOut=setTimeout(function(){checkCPUandGPU(false)}, 8000);
		$( "#select-cpu .oi-magnifying-glass" ).click(function() {

				$('#cpu-model').trigger('change');
			});
		$( "#select-gpu .oi-magnifying-glass" ).click(function() {

			$('#gpu-model').trigger('change');
		});
		$( "#select-game .oi-magnifying-glass" ).click(function() {

			$('#game').trigger('change');
		});
		$('#game').change(function(){
			var str=$('#game').val();
			updateGameList(str,false);
			
		});
		//$('#game').trigger('change');
		$('#cpu-brand li a p.choice').click(function(){
			var cpuBrand=$(this).text()+"";
			if (cpuBrand != presentCPU){
				$('#cpu-model-name ul').html("<p style='color:red;'>Loading...</p><div class='loaderContainer'><div class='loaderInner'><div class='loader'></div></div></div>");
				var completeCPUHTML = document.createElement("ul");
				completeCPUHTML=$(completeCPUHTML);
				if (cpuBrand=="Intel"){var tempList=cpuList[0];}
				else if (cpuBrand=="AMD"){var tempList=cpuList[1];}
				else{var tempList=[];}
				for (var i=0;i<tempList.length;i++){

					var newli="<li class='list-group-item'><a>"+tempList[i]+"</a></li>";
					newli=$(newli);
					newli.click(function(){
						var cpuName=$(this).text()+"";
						console.log('Selected '+cpuName);
						var newElement="<span class='selected'>"+cpuName+"</span>";
						$('#select-cpu p.col-sm-10').html(newElement);
						$('#cpu-brand').collapse("hide");
						$('#cpu-model-name').collapse("hide");
					});

					completeCPUHTML.append(newli);

				}
				presentCPU=cpuBrand;
				presentCPUList=tempList;

				$('#cpu-model-name ul').html("")
				completeCPUHTML.children().each(function () {

					$('#cpu-model-name ul').append($(this)); //log every element found to console output
				});

			}
			$('#cpu-model-name').collapse('show');
		});
		$('#cpu-model').change(function(){
			var cnt=0;
			var str=$(this).val();
			$('#cpu-model-name ul').html("");
			for (var i=0;i<presentCPUList.length;i++){
				if ((presentCPUList[i]+"").toUpperCase().includes(str.toUpperCase())){
					var newli="<li class='list-group-item'><a>"+presentCPUList[i]+"</a></li>";
					newli=$(newli)
					newli.click(function(){
						var cpuName=$(this).text()+"";
						console.log('Selected '+cpuName);
						var newElement="<span class='selected'>"+cpuName+"</span>";
						$('#select-cpu p.col-sm-10').html(newElement);
						$('#cpu-brand').collapse("hide");
						$('#cpu-model-name').collapse("hide");
					});
					$('#cpu-model-name ul').append(newli);
				cnt+=1;
				}
				if(cnt>=7) break;
			}
			if (cnt==0){
				var newli="<li class='list-group-item'>Nothing Found</li>";
				$('#cpu-model-name ul').append(newli);
			}			
		});
		$('#gpu-brand li a p.choice').click(function(){
			var gpuBrand=$(this).text()+"";
			if (gpuBrand != presentGPU){
				$('#gpu-model-name ul').html("<p style='color:red;'>Loading...</p><div class='loaderContainer'><div class='loaderInner'><div class='loader'></div></div></div>");
				var completeGPUHTML = document.createElement("ul");
				completeGPUHTML=$(completeGPUHTML);
				if (gpuBrand=="Nvidia"){var tempList=gpuList[0];}
				else if (gpuBrand=="AMD"){var tempList=gpuList[1];}
				else{var tempList=[];}

				for (var i=0;i<tempList.length;i++){
					var newli="<li class='list-group-item'><a>"+tempList[i]+"</a></li>";
					newli=$(newli)
					newli.click(function(){
						var gpuname=$(this).text()+"";
						console.log('Selected '+gpuname);
						var newElement="<span class='selected'>"+gpuname+"</span>";
						$('#select-gpu p.col-sm-10').html(newElement);
						$('#gpu-brand').collapse("hide");
						$('#gpu-model-name').collapse("hide");
					});
					completeGPUHTML.append(newli);
					
				}
				presentGPU=gpuBrand;
				presentGPUList=tempList;
				$('#gpu-model-name ul').html("")
				completeGPUHTML.children().each(function () {

					$('#gpu-model-name ul').append($(this)); //log every element found to console output
				});

			}
			$('#gpu-model-name').collapse('show');
		});
		$('#gpu-model').change(function(){
			var cnt=0
			var str=$(this).val();
			$('#gpu-model-name ul').html("");
			for (var i=0;i<presentGPUList.length;i++){
				if ((presentGPUList[i]+"").toUpperCase().includes(str.toUpperCase())){
					var newli="<li class='list-group-item'><a>"+presentGPUList[i]+"</a></li>";
					newli=$(newli)
					newli.click(function(){
						var gpuname=$(this).text()+"";
						console.log('Selected '+gpuname);
						var newElement="<span class='selected'>"+gpuname+"</span>";
						$('#select-gpu p.col-sm-10').html(newElement);
						$('#gpu-brand').collapse("hide");
						$('#gpu-model-name').collapse("hide");
					});
					$('#gpu-model-name ul').append(newli);
				cnt+=1
				}
				if(cnt>=7) break;
			}
			if (cnt==0){
				var newli="<li class='list-group-item'>Nothing Found</li>";
				$('#gpu-model-name ul').append(newli);
			}			
		});
		$('#select-cpu').click(function(){
			var collapsed=$('#cpu-brand').hasClass('collapse')
			if (collapsed){
				$('#cpu-brand').collapse("show");
				$('#cpu-model-name').collapse("hide");
			}else{
				$('#cpu-brand').collapse("hide");
				$('#cpu-model-name').collapse("hide");
			}
		});
		$('#select-gpu').click(function(){
			var collapsed=$('#gpu-brand').hasClass('collapse')
			if (collapsed){
				$('#gpu-brand').collapse("show");
				$('#gpu-model-name').collapse("hide");
			}else{
				$('#gpu-brand').collapse("hide");
				$('#gpu-model-name').collapse("hide");
			}
		});
		
		$('#predict-button').click(function(){
			$('#display-column').html("<p style='color:red;'>Loading...</p><div class='loaderContainer'><div class='loaderInner'><div class='loader'></div></div></div>");
			args=[]
			args.push($("#select-cpu span.selected").text());
			args.push($("#select-gpu span.selected").text());
			args.push($("#select-game span.selected").text());
			args.push($("#ram").val());
			args.push($("#width").val());
			args.push($("#height").val());
			var setting= $("#setting").val();
			setting=setting.charAt(0).toUpperCase()+setting.slice(1);
			
			args.push(setting)
			for (var i=0;i<args.length;i++){
				if (args[i].length<=0){
					$('#display-column').html("<span style='color:red'>Please enter all columns</span>");
					return;
				}
				console.log(args[i]);
			}
			/*
			$.ajax({
					type: "POST",
					//would be change later
					//url: "http://localhost:8080/predict/cpu="+args[0]+"&gpu="+args[1]+"&game="+args[2]+"&resWidth="+args[4]+"&resHeight="+args[5]+"&setting="+args[6]+"&ram="+args[3],
					url: "http://localhost:8080/predict/",
					contentType: "application/json; charset=utf-8",
					data: {name: "Donald Duck",city: "Duckburg"},
					dataType: "json",
					success: function (response) {
						console.log(response);
					},
					failure: function (response) {
						console.log("Unable to connect Database");
					},
					error: function (response) {
						console.log("Unable to connect Database");
					}
				});
				*/
			$.ajax({
				type: "POST",
				url: "<%=normalPath%>:5000/predict",
				contentType: "application/json; charset=utf-8",
				dataType: "json",
				data: {
						cpu: args[0],
							gpu: args[1],
							game: args[2],
							setting:args[6],
							resWidth:args[4],
							resHeight:args[5],
							ram:args[3]
						},
				success: function (response) {
						console.log(response);
						console.log(response['result']);
						$('#display-column').html("<span style='color:blue;text-decoration-line: underline; text-decoration-style: wavy;'>"+response['result']+"</span>");		
					},
				failure: function (response) {
					console.log(response)
					//console.log("Failed: "+response['responseText']);
				//	var response=response.responseText;
					//response=response.replace(/\"/g,"");
					$('#display-column').html("<span style='color:red'>Unable to call service</span>");
				},
				error: function (response) {
					console.log(response);
					console.log("Failed: "+response['responseText']);
					if(response['responseText']==null){
						$('#display-column').html("<span style='color:red'>Unable to call service</span>");
					}
					else{
					$('#display-column').html("<span style='color:red'>"+response['responseText']+"</span>");
					}
				}
			});
		});
		$("#setting").autocomplete({source:["Low","Medium","High","Ultra"]});
		
	
	});
</script>
</head>
<body>
<header>

<div class="wrapper">
<div class="container-fluid">
	<div class="row">
		<div class="col-7 col-offset-2-1-2 col-md-3 col-lg-1">
			<div style="background-color:#DBD8E0;"><a href="index"><img id="nav-logo" class="responsive" src="../resources/logo.png"></img></a></div>
		</div>
				<div class="col-12">
<div class="autoDisableForMobile" style="width:100%;height:1px;background-color:#C9C5C2"></div>
</div>
		<div class="col-12 col-md-9 col-lg-11 nav-wrapper">
			<nav>
				<ul class="list-inline">
				
				  <li class="list-inline-item list-inline-item-success"><span class="main-nav"><a href="index">Home</a></span></li>
				  <li class="list-inline-item list-inline-item-info"><a href="#">FPS Estimator</a></li>
				</ul>
			</nav>
		</div>
	</div>
</div>
</div>
<div style="width:100%;height:1px;margin-top:2px;background-color:#C9C5C2"></div>
<div style="width:100%;height:1px;background-color:#918E8C;"></div>
<div style="width:100%;height:1px;background-color:#C9C5C2"></div>
</header>
<section>
<!-- 
<div id="loader-wrapper">
    <div id="loader"></div>
 
    <div class="loader-section section-left"></div>
    <div class="loader-section section-right"></div>
 
</div>
 -->
<div class="wrapper">
<div class="container-fluid">
	<div id="guide">
		<h1>Using Guide</h1>
		<div class="row">
			<div class="col-xs-12 col-sm-6 col-lg-5 col-xl-4">
				<p>Step 1: Select CPU Model</p>
				<p>Step 1(a): Select CPU Brand</p>
				<p>Step 1(b): Enter CPU Model Name for searching</p>
				<p>Step 1(c): Click for the correct CPU Model</p>
				<p>Step 2: Select Graphic Card Model</p>
			</div>
			<div class="col-xs-12 col-sm-6 col-lg-5 col-xl-4">
				<p>Step 3: Select Game (Only First 7 Game shown)</p>
				<p>Step 4: Enter the GB of Ram wanted to estimate</p>
				<p>Step 5: Fill in the Resolution information</p>
				<p>Step 6: Fill in the basic setting of the game (<span class="settingRemark">Low</span>/<span class="settingRemark">Medium</span>/<span class="settingRemark">High</span>/<span class="settingRemark">Ultra</span>)</p>
				<p>Step 7: Click on "Predict" button for running FPS Estimator</p>
			</div>
		</div>
	</div>
	<div class="row">
		<div class="col-sm-12 col-md-8 col-lg-9 col-xl-8 main-select-col">
			<div class="select-cpu row">
				<div class="col-md-4 col-lg-2 description"><h4>CPU :</h4></div>
				<div class="col-md-6 col-lg-10 row selection">
				  <div id="select-cpu" class="col-md-12 col-lg-4 ">
					<button class="btn btn-primary select-btn" type="button" data-toggle="collapse" data-target="#cpu-brand" style="width:100%;display:flex;">
						<p class="col-sm-10">Select CPU</p>
						<span class="oi oi-chevron-right col-sm-2" style="padding-left:0px;"></span>
					</button>
				  </div>
				  <div id="cpu-brand" class="col-md-12 col-lg-4 collapse">
					<div class="dropdown-list">
					<p>Select Brand</p>
					<ul class="list-group">
						<li class="list-group-item"><a class="unchecked">
					  		<div class="inner-addon right-addon">
								<span class="oi oi-circle-x"></span>
								<p class="choice">Intel</p>
							</div>
						</a></li>
					  	<li class="list-group-item"><a class="unchecked">
						  	<div class="inner-addon right-addon">
						  		<span class="oi oi-circle-x"></span>							
						  		<p class="choice">AMD</p>
						  	</div>
					  	</a></li>
					</ul>
					</div>
				  </div>
				  <div id="cpu-model-name" class="col-md-12 col-lg-4 collapse">
		 				<div class="dropdown-list">
		<div class="inner-addon right-addon">
<a><span class="oi oi-magnifying-glass"></span></a>
					<input type="text" class="form-control" id="cpu-model" placeholder="Enter Model"/>
					</div>
					<ul class="list-group">
					  <li class="list-group-item">Core i3-2100</li>
					  <li class="list-group-item">Core i3-2100K</li>
					  <li class="list-group-item">Core i5-8500</li>
					</ul>
					</div>
				  </div>
				</div>
			</div>
			<div class="select-gpu row">
				<div class="col-md-4 col-lg-2 description"><h4>GPU :</h4></div>
				<div class="col-md-6 col-lg-10 row selection">
					<div id="select-gpu" class="col-md-12 col-lg-4 ">
						<button class="btn btn-primary select-btn" type="button" data-toggle="collapse" data-target="#gpu-brand">
							<p class="col-sm-10" style="word-wrap:break-word;">Select Graphic Card</p>
							<span class="oi oi-chevron-right col-sm-2" style="padding-left:0px;"></span>
						</button>
					  </div>
					  <div id="gpu-brand" class="col-md-12 col-lg-4 collapse">
						<div class="dropdown-list">
						<p>Select Brand</p>
						<ul class="list-group">
					  	<li class="list-group-item"><a class="unchecked">
						  	<div class="inner-addon right-addon">
						  		<span class="oi oi-circle-x"></span>							
						  		<p class="choice">Nvidia</p>
						  	</div>
					  	</a></li>
					  	<li class="list-group-item"><a class="unchecked">
						  	<div class="inner-addon right-addon">
						  		<span class="oi oi-circle-x"></span>							
						  		<p class="choice">AMD</p>
						  	</div>
					  	</a></li>
						</ul>
						</div>
					  </div>
					  <div id="gpu-model-name" class="col-md-12 col-lg-4 collapse">
						<div class="dropdown-list">
								<div class="inner-addon right-addon">
<a><span class="oi oi-magnifying-glass"></span></a>
						<input type="text" class="form-control" id="gpu-model" placeholder="Enter Model">
						</div>
						<ul class="list-group">
						  <li class="list-group-item">GeForce GTX 1080</li>
						  <li class="list-group-item">GeForce GTX 1070</li>
						  <li class="list-group-item">GeForce GTX 1060</li>
						</ul>
						</div>
					</div>
				</div>
			</div>
			<div class="select-game row">
				<div class="col-md-4 col-lg-2 description"><h4>Game :</h4></div>
				<div class="col-md-6 col-lg-10 row selection">
					<div id="select-game" class="col-md-12 col-lg-4">
						<button class="btn btn-primary select-btn unchecked" type="button" data-toggle="collapse" data-target="#game-name" style="width:100%;display:flex;">
							<p class="col-sm-10">Select Game</p>
							<span class="oi oi-circle-x col-sm-2 loading-icon" style="padding-left:0px;"></span>
							<span class="oi oi-chevron-right col-sm-2 invisible-icon" style="padding-left:0px;"></span>
						</button>
					</div>
					<div id="game-name" class="col-md-12 col-lg-4 collapse">
						<div class="dropdown-list">
								<div class="inner-addon right-addon">
<a><span class="oi oi-magnifying-glass"></span></a>
						<input type="text" class="form-control" id="game" placeholder="Enter Game Name">
						</div>
						<ul class="list-group">
						  <li class="list-group-item">Just Cause 3</li>
						  <li class="list-group-item">Battlefield 1</li>
						</ul>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="col-sm-12 col-md-4 col-lg-3 col-xl-2 col-xl-offset-1 another-select-col">
		<!--	<div class="input-ram" style="background-color:grey;">-->
			<form class="form-horizontal">
			  <div class="form-group row">
				<label class="control-label col-sm-4" for="ram">Ram<span class="partial-visible"> (GB)</span>:</label>
				<div class="col-sm-8">
				  <input type="number" class="form-control" id="ram" placeholder="Enter Here">
				</div>
			  </div>
			  <div class="form-group row">
				<label class="control-label col-sm-12" for="width">Resolution<span class="partial-visible"> (px)</span>:</label>
				<div class="col-sm-12 resolution-input">
					<div class="row" style="max-width:100%;margin-left:0px;">
						<div class="col-sm-5">
							<input type="number" class="form-control" id="width" placeholder="Width">
						</div>
						<div class="col-sm-2" style="text-align:center;">
							<label class="control-label" for="height">X</label>
						</div>
						<div class="col-sm-5"> 
							<input type="number" class="form-control" id="height" placeholder="Height">
						</div>
					</div>
				</div>
			  </div>
			  <div class="form-group row">
				<label class="control-label col-sm-4" for="setting">Setting:</label>
				<div class="col-sm-8">
				  <input type="text" class="form-control" id="setting" placeholder="Enter Here">
				</div>
			  </div>
			<!--  <div class="form-group">
				<label class="control-label col-sm-8" for="height">Height Resolution:</label>
				<div class="col-sm-4"> 
				  <input type="number" class="form-control" id="height" placeholder="Enter password">
				</div>
			  </div>
			  -->
			  <div class="form-group row"> 
				<div class="col-sm-12 col-md-8 col-md-offset-2">
					<button id="predict-button" type="button" class="btn btn-danger" style="width:100%;height:auto; background-color:#5C1717;">Predict</button>
				  <!-- <button type="submit" class="btn btn-default">Submit</button> -->
				</div>
			  </div>
			</form>
			<div id="display-column">
			</div>
			<!--<div class="another-select-col-label"><p>Ram (GB):</p></div>
			<div class="another-select-col-value"><input type="number" placeholder="Input Here" name="ram"></div>
			-->
			<!--
			</div>
			<div class="input-width" style="background-color:grey;">
			<div class="another-select-col-label"><p>Width Resolution (px):</p></div>
			<div class="another-select-col-value"><input type="number" placeholder="Input Here" name="res-width"></div>
			</div>
			<div class="input-height" style="background-color:grey;">
			<div class="another-select-col-label"><p>Height Resolution (px):</p></div>
			<div class="another-select-col-value"><input type="number" placeholder="Input Here" name="res-height"></div>
			</div>
			<div class="submit-button" style="height:50px; text-align:center; vertical-align:center; margin-top:20px;">
			<div class="center" style="	text-align:center;">
			<button type="button" class="btn btn-danger" style="width:70%;height:auto; background-color:#5C1717;">Danger</button>
			</div>
			</div>
			-->
		</div>
	</div>
</div>
</div>
</section>
<footer>
<div class="wrapper">
<p>Copyright@<span style="font-weight: bold;">Long Yau</span>	2018-2018</p>
<p>Teesside University Assignment All rights reserved</p>
</div>
</footer>
</body>