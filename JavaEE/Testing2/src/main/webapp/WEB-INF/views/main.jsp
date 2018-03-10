<!DOCTYPE HTML>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FPS Predictor</title>
<!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
-->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

 <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.17.0/jquery.validate.min.js"></script>

<style>
header{
/*background-color:#918E8C;*/
}
footer{
background-color:#918E8C;
padding-bottom:10px;
}
header .row{
	position:relative;
}
div.nav-wrapper{
position:absolute;
bottom:0px;
right:0px;
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
nav ul li:hover{
background-color:grey !important;
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
/*
.another-select-col-value{
	width:35%;
	padding-right:5%;
   display: flex;
   justify-content: center;
   align-items:center;
	vertical-align:middle;
}
.another-select-col-value input{
	width: 100%;
	height: auto;
	margin: 3px 0px;
	vertical-align:middle;
}
*/
button.select-btn{
width:100%;
display:flex;
white-space:normal !important;
word-wrap: break-word;
}
header .wrapper{
width:90%;
margin-left:5%;
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
	var presentCPU="";
		var gpuList=[];
	var presentGPU="";
	$( document ).ready(function() {
		$('#game').change(function(){
			var str=$('#game').val();
			$.ajax({
				type: "GET",
				//would be change later
				url: "http://localhost:8081/fpsestimator/Game/Partial?input="+str+"&limit=7",
				contentType: "application/json; charset=utf-8",
				dataType: "json",
				success: function (response) {
					console.log(response);
					i = 0;
					$('#game-name ul').html("");
					if (response!=null&&response.length !=0) {
						while (response[i] != null) {
							var newli="<li class='list-group-item'><a>"+response[i].Name+"</a></li>";
							newli=$(newli)
							newli.click(function(){
								var gamename=$(this).text()+"";
								console.log('Selected '+gamename);
								var newElement="<span class='selected'>"+gamename+"</span>";
								$('#select-game p.col-sm-10').html(newElement);
								$('#game-name').collapse("hide");
							});
							$('#game-name ul').append(newli);
							i++;
						};
					}else{
						var newli="<li class='list-group-item'>Nothing Found</li>";
						$('#game-name ul').append(newli);
					}
				},
				failure: function (response) {
					console.log("Unable to connect Database");
				},
				error: function (response) {
					console.log("Unable to connect Database");
				}
			});
		});
		$('#game').trigger('change')
		$('#cpu-brand li').click(function(){
			var cpuBrand=$(this).text()+"";
			if (cpuBrand != presentCPU){
				$.ajax({
					type: "GET",
					//would be change later
					url: "http://localhost:8081/fpsestimator/CPU/"+cpuBrand,
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					success: function (response) {
						console.log(response);
						var i = 0;
						if (response!=null&&response.length !=0) {
							cpuList=[]
							while (response[i] != null) {	
								var temp = response[i].Name+"";
								cpuList.push(temp);
								i++;
							};
						$('#cpu-model-name ul').html("");
						for (var i=0;i<7;i++){
							if (i<=cpuList.length){
								var newli="<li class='list-group-item'><a>"+cpuList[i]+"</a></li>";
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
							}
						}
						
						presentCPU=cpuBrand;
						}
					},
					failure: function (response) {
						console.log("Unable to connect Database");
					},
					error: function (response) {
						console.log("Unable to connect Database");
					}
				});
			}
			$('#cpu-model-name').collapse('show');
		});
		$('#cpu-model').change(function(){
			var cnt=0
			var str=$(this).val();
			$('#cpu-model-name ul').html("");
			for (var i=0;i<cpuList.length;i++){
				if ((cpuList[i]+"").startsWith(str)){
					var newli="<li class='list-group-item'><a>"+cpuList[i]+"</a></li>";
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
				cnt+=1
				}
				if(cnt>=7) break;
			}
			if (cnt==0){
				var newli="<li class='list-group-item'>Nothing Found</li>";
				$('#cpu-model-name ul').append(newli);
			}			
		});
		$('#gpu-brand li').click(function(){
			var gpuBrand=$(this).text()+"";
			if (gpuBrand != presentGPU){
				$.ajax({
					type: "GET",
					//would be change later
					url: "http://localhost:8081/fpsestimator/GPU/"+gpuBrand,
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					success: function (response) {
						console.log(response);
						var i = 0;
						if (response!=null&&response.length !=0) {
							gpuList=[]
							while (response[i] != null) {	
								var temp = response[i].Name+"";
								gpuList.push(temp);
								i++;
							};
						$('#gpu-model-name ul').html("");
						for (var i=0;i<7;i++){
							if (i<=gpuList.length){
								var newli="<li class='list-group-item'><a>"+gpuList[i]+"</a></li>";
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
							}
						}
						presentGPU=gpuBrand;
						}
					},
					failure: function (response) {
						console.log("Unable to connect Database");
					},
					error: function (response) {
						console.log("Unable to connect Database");
					}
				});
			}
			$('#gpu-model-name').collapse('show');
		});
		$('#gpu-model').change(function(){
			var cnt=0
			var str=$(this).val();
			$('#gpu-model-name ul').html("");
			for (var i=0;i<gpuList.length;i++){
				if ((gpuList[i]+"").startsWith(str)){
					var newli="<li class='list-group-item'><a>"+gpuList[i]+"</a></li>";
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
			args=[]
			args.push($("#select-cpu span.selected").text());
			args.push($("#select-gpu span.selected").text());
			args.push($("#select-game span.selected").text());
			args.push($("#ram").val());
			args.push($("#width").val());
			args.push($("#height").val());
			args.push($("#setting").val());
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
				url: "http://localhost:5000/predict",
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
						$('#display-column').html("<span style='color:blue'>"+response['result']+"</span>");		
					},
				failure: function (response) {
					console.log("Failed: "+response.responseText);
					var response=response.responseText;
					response=response.replace(/\"/g,"");
					$('#display-column').html("<span style='color:red'>"+response+"</span>");
				},
				error: function (response) {
					console.log("Failed: "+response.responseText);
					var response=response.responseText;
					response=response.replace(/\"/g,"");
					$('#display-column').html("<span style='color:red'>"+response+"</span>");
				}
			});
		});
	});
</script>
</head>
<body>
<header>
<div class="wrapper">
<div class="container-fluid">
	<div class="row">
		<div class="col-xs-3 col-sm-2">
			<div style="height:100px; background-color:grey;"></div>
		</div>
		<div class="col-xs-9 col-sm-10 nav-wrapper">
			<nav>
				<ul class="list-inline">
				  <li class="list-inline-item list-inline-item-success"><span class="main-nav">Home</span></li>
				  <li class="list-inline-item list-inline-item-info">Second item</li>
				  <li class="list-inline-item list-inline-item-warning">Third item</li>
				  <li class="list-inline-item list-inline-item-danger">Fourth item</li>
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
		<div class="col-xs-12 col-sm-8 main-select-col">
			<div class="select-cpu row" style=" background-color:grey;">
			  <div id="select-cpu" class="col-sm-4">
				<button class="btn btn-primary select-btn" type="button" data-toggle="collapse" data-target="#cpu-brand" style="width:100%;display:flex;">
				<p class="col-sm-10">Select CPU</p>
				<span class="glyphicon glyphicon-play col-sm-2" style="padding-left:0px;"></span></button>
			  </div>
			  <div id="cpu-brand" class="col-sm-4 collapse">
				<div class="dropdown-list">
				<p>Select Brand</p>
				<ul class="list-group">
				  <li class="list-group-item"><a href="#">Intel</a></li>
				  <li class="list-group-item"><a href="#">AMD</a></li>
				</ul>
				</div>
			  </div>
			  <div id="cpu-model-name" class="col-sm-4 collapse">
  				<div class="dropdown-list">

				<input type="text" class="form-control" id="cpu-model" placeholder="Enter Model">
				<ul class="list-group">
				  <li class="list-group-item"><a href="#">Core i3-2100</a></li>
				  <li class="list-group-item"><a href="#">Core i3-2100K</a></li>
				  <li class="list-group-item"><a href="#">Core i5-8500</a></li>
				</ul>
				</div>
			  </div>
			</div>
			<div class="select-gpu row" style="background-color:grey;">
				<div id="select-gpu" class="col-sm-4">
					<button class="btn btn-primary select-btn" type="button" data-toggle="collapse" data-target="#gpu-brand">
					<p class="col-sm-10" style="word-wrap:break-word;">Select Graphic Card</p>
					<span class="glyphicon glyphicon-play col-sm-2" style="padding-left:0px;"></span>
					</button>
				  </div>
				  <div id="gpu-brand" class="col-sm-4 collapse">
					<div class="dropdown-list">
					<p>Select Brand</p>
					<ul class="list-group">
					  <li class="list-group-item"><a href="#">Nvidia</a></li>
					  <li class="list-group-item"><a href="#">AMD</a></li>
					</ul>
					</div>
				  </div>
				  <div id="gpu-model-name" class="col-sm-4 collapse">
					<div class="dropdown-list">
					<input type="text" class="form-control" id="gpu-model" placeholder="Enter Model">
					<ul class="list-group">
					  <li class="list-group-item"><a href="#">GeForce GTX 1080</a></li>
					  <li class="list-group-item"><a href="#">GeForce GTX 1070</a></li>
					  <li class="list-group-item"><a href="#">GeForce GTX 1060</a></li>
					</ul>
					</div>
				</div>
			</div>
			<div class="select-game row" style="background-color:grey;">
				<div id="select-game" class="col-sm-4">
					<button class="btn btn-primary select-btn" type="button" data-toggle="collapse" data-target="#game-name" style="width:100%;display:flex;">
					<p class="col-sm-10">Select Game</p>
					<span class="glyphicon glyphicon-play col-sm-2" style="padding-left:0px;"></span></button>
				</div>
				<div id="game-name" class="col-sm-4 collapse">
					<div class="dropdown-list">
					<input type="text" class="form-control" id="game" placeholder="Enter Game Name">
					<ul class="list-group">
					  <li class="list-group-item"><a href="#">Just Cause 3</a></li>
					  <li class="list-group-item"><a href="#">Battlefield 1</a></li>
					</ul>
					</div>
				</div>
			</div>
		</div>
		<div class="col-xs-12 col-sm-4 another-select-col">
		<!--	<div class="input-ram" style="background-color:grey;">-->
			<form class="form-horizontal">
			  <div class="form-group">
				<label class="control-label col-sm-4" for="ram">Ram:</label>
				<div class="col-sm-8">
				  <input type="number" class="form-control" id="ram" placeholder="Enter Here">
				</div>
			  </div>
			  <div class="form-group">
				<label class="control-label col-sm-4" for="width">Resolution:</label>
				<div class="col-sm-8 resolution-input">
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
			  <div class="form-group">
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
			  <div class="form-group"> 
				<div class="col-sm-offset-2 col-sm-8">
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