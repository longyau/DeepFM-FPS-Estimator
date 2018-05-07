<!DOCTYPE HTML>
<%
    //String path = request.getContextPath();
	String normalPath=request.getScheme()+"://"+request.getServerName();
   // String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
    //String menuPath=request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+"/website/";
%>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FPS Estimator - Index</title>
<link rel="shortcut icon" href="../resources/icon/favicon.ico" />
<!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
-->
  <link rel="stylesheet" href="../resources/css/bootstrap.min.css">

 <script src="../resources/js/jquery.min.js"></script>
   <script src="../resources/js/tether.min.js"></script>
  <script src="../resources/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.17.0/jquery.validate.min.js"></script>
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-118399528-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-118399528-1');
</script>

<style>
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
width:80%;
margin-left:10%;
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
padding-bottom:20px;
}
#main-content h1{
text-align:left;
margin-bottom:1rem;
}
#main-content h2,#main-content h3,#main-content p{
text-align:left;
margin-bottom:0.5rem;
}
#main-content h1{
color:#142D42;
text-decoration:underline;
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
@media (min-width:960px){
.col-lg-offset-1-1-2{
margin-left:12.5%;
}
.col-lg-offset-1-2{
margin-left:4%;
}
}
@media (min-width:576px){
.col-sm-offset-1-2{
margin-left:4%;
}

}
@media (max-width:576px){
.col-offset-2{
margin-left:16.66666%;
}
.col-offset-2-1-2{
margin-left:20.8333333%;
}

}
</style>
<script>
</script>
</head>
<body>
<header>
<div class="wrapper">
<div class="container-fluid">
	<div class="row">
		<div class="col-7 col-offset-2-1-2 col-md-3 col-lg-1">
			<div style="background-color:#DBD8E0;"><a href="#"><img id="nav-logo" class="responsive" src="../resources/logo.png"></img></a></div>
		</div>
				<div class="col-12">
<div class="autoDisableForMobile" style="width:100%;height:1px;background-color:#C9C5C2"></div>
</div>
		<div class="col-12 col-md-9 col-lg-11 nav-wrapper">
			<nav>
				<ul class="list-inline">
				
				  <li class="list-inline-item list-inline-item-success"><span class="main-nav"><a href="#">Home</a></span></li>
				  <li class="list-inline-item list-inline-item-info"><a href="fpsestimator">FPS Estimator</a></li>
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
<div class="wrapper">
<div class="container-fluid">
	<div class="row">
		<div id="main-content" class="col-lg-11 col-lg-offset-1-2">
			<div class="row"><div class="col-sm-12">
			<h1>About this website</h1>
			</div></div>
			<div class="row"><div class="col-sm-11 col-sm-offset-1-2">
			<p>This website provides FPS Estimator for facilitating PC-gamers while choosing compoenets.</p>
			</div></div>
			<div class="row"><div class="col-sm-11 col-sm-offset-1-2">
			<p>This website will estimate Frames-Per-Seconds(FPS) result of different PC components,users could enter different configuration and get the predicted FPS result.</p>
			</div></div>
			<div class="row"><div class="col-sm-11 col-sm-offset-1-2">
			<p>This estimator is based on DeepFM, which is a combination of Deep-Neural Network and Factorization Machine*.</p>
			</div></div>
			<div class="row"><div class="col-sm-11 col-sm-offset-1-2">
			<p class="references">*Reference: DeepFM: A Factorization-Machine based Neural Network for CTR</p>
			</div></div>
			<div class="row"><div class="col-sm-11 col-sm-offset-1-2">
			<p style="color:#142D42;">This website is a part of Academic Passage, written on "Building FPS Estimator System based on Machine Learning".</p>
			</div></div>
		</div>
	</div>
	<div class="row">
			<div id="other-content" class="col-lg-9 col-lg-offset-1-1-2">
				<div class="row">
					<div id="other-content-carousel" class="carousel slide col-sm-12" data-ride="carousel">
					  <ol class="carousel-indicators">
					    <li data-target="#other-content-carousel" data-slide-to="0" class="active"></li>
					    <li data-target="#other-content-carousel" data-slide-to="1"></li>
					  </ol>
					  <div class="carousel-inner" role="listbox">
					    <div class="carousel-item active">
					    	<div style="display:block;width:100%;">
							<div class="row"><div class="col-sm-12"><h1 style="text-align:center;">What is FPS?</h1></div></div>
							<div class="row"><div class="col-sm-12"><p>Frames per second (FPS) is a unit that measures display device performance. It consists of the number of complete scans of the display screen that occur each second. This is the number of times the image on the screen is refreshed each second, or the rate at which an imaging device produces unique sequential images called frame*</p></div></div>
							<div class="row"><div class="col-sm-12"><img class="responsive" style="display: block;margin-left: auto;margin-right: auto;width: 75%;" src="../resources/images/fpsillustration.png"/></div></div>
											<div class="row"><div class="col-sm-12"><span class="references">*Reference: https://www.techopedia.com/definition/7297/frames-per-second-fps</span></div></div>
							<div class="row"><div class="col-sm-12"><span class="references">Reference: http://blog.logicalincrements.com/2014/06/frames-per-second-5-simple-tips-to-boost-your-fps/</span></div></div>
							</div>
					    </div>
					    <div class="carousel-item">
					      	<div style="display:block;width:100%;">
							<div class="row"><div class="col-sm-12"><h1 style="text-align:center;">What do FPS means in gaming?</h1></div></div>
							<div class="row"><div class="col-sm-12"><p>FPS means how smoothly the game runs without any hiccups. The more the FPS of the game while functioning, the better is the experience. You can feel the difference while playing yourself. 60 FPS is, for gamers, an ideal situation. But you can always strive for more!*</p></div></div>
							<div class="row"><div class="col-sm-12"><span class="references">*Reference: https://www.quora.com/What-is-an-FPS-in-gaming</span></div></div>
							<div class="row"><div class="col-sm-12"><p>Watch a video for comparison</p></div></div>
							<div class="row"><div class="col-12 col-sm-9 col-sm-offset-1-2"><div class="videoWrapper"><iframe src="https://www.youtube.com/embed/rx704_XjGRM" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div></div></div>
							<div class="row"><div class="col-sm-12"><span class="references">Reference: https://www.youtube.com/watch?v=rx704_XjGRM</span></div></div>
							</div>
					    </div>
					    <!-- 
					    <div class="carousel-item">
					      <img class="d-block img-fluid" src="..." alt="Third slide">
					    </div> -->
					  </div>
					  <a class="carousel-control-prev" href="#other-content-carousel" role="button" data-slide="prev">
					    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
					    <span class="sr-only">Previous</span>
					  </a>
					  <a class="carousel-control-next" href="#other-content-carousel" role="button" data-slide="next">
					    <span class="carousel-control-next-icon" aria-hidden="true"></span>
					    <span class="sr-only">Next</span>
					  </a>
					</div>
				</div>
			</div>
	</div>
		<div class="row">
		<div class="col-lg-11 col-lg-offset-1-2">
		<p>Please fill in a google response form: <a href="https://goo.gl/forms/esGHG5dbJRaVDxKE3">Click Here</a></p>
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