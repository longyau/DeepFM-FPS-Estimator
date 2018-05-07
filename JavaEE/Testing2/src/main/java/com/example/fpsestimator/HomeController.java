package com.example.fpsestimator;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.util.Iterator;
import java.util.Map;

import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonArrayBuilder;
import javax.json.JsonReader;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Index;
import com.amazonaws.services.dynamodbv2.document.Item;
import com.amazonaws.services.dynamodbv2.document.ItemCollection;
import com.amazonaws.services.dynamodbv2.document.QueryOutcome;
import com.amazonaws.services.dynamodbv2.document.Table;
import com.amazonaws.services.dynamodbv2.document.spec.QuerySpec;
import com.amazonaws.services.dynamodbv2.document.utils.NameMap;
import com.amazonaws.services.dynamodbv2.document.utils.ValueMap;

/**
 * Handles requests for the application home page.
 */
@RestController
public class HomeController {
	
	private static final Logger logger = LoggerFactory.getLogger(HomeController.class);
	private AmazonDynamoDB dynamoDB;
    private static final String hardwareTable="FYP_Hardware";
    private Runtime runtime=Runtime.getRuntime();
    public void init() {
        AWSCredentials credentials = null;
	    try {
	        credentials = new ProfileCredentialsProvider("default").getCredentials();
	    } catch (Exception e) {
	        throw new AmazonClientException(
	                "Cannot load the credentials from the credential profiles file. " +
	                "Please make sure that your credentials file is at the correct " +
	                "location (C:\\Users\\long1\\.aws\\credentials), and is in valid format.",
	                e);
	    }
	    dynamoDB = new AmazonDynamoDBClient(credentials);
	    Region usEast2 = Region.getRegion(Regions.US_EAST_2);
	    dynamoDB.setRegion(usEast2);
	   // dynamoDB.setRegion(usWest2);
	    
	    try {
			Process p = runtime.exec("python FYP-predictFPS2.py");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
    public HomeController(){
    	init();
    }
    private JsonArray getAllData(String type) {
    	return this.getAllData(type, "");
    }
   	private JsonArray getAllData(String type,String brand){
   		JsonArrayBuilder output=Json.createArrayBuilder();
   		DynamoDB _dynamoDB = new DynamoDB(dynamoDB);
   		Table table = _dynamoDB.getTable(hardwareTable);
   		Index index=null;
   		if (brand!=""){
	   		index= table.getIndex("Type-Brand-index");
   		}
   		Map<String,Object> vm= new ValueMap().withString(":v_id", type);
   		if (brand!=""){
   		vm.put(":sk_id", brand);
  		}
   		Map<String, String> nm= new NameMap();
   		nm.put("#pk_col","Type");
   		if (brand!=""){
   		nm.put("#sk_col","Brand");
   		nm.put("#show_col", "Name");
  		}else {
  		nm.put("#sk_col", "Name");
  		}

  		
  		String kce="#pk_col=:v_id";
   		if (brand!=""){
  			kce+=" AND #sk_col =:sk_id";
  		}
  		QuerySpec spec = new QuerySpec()
  		    .withKeyConditionExpression(kce)
  		    .withNameMap(nm)
  		    .withValueMap(vm);
  		ItemCollection<QueryOutcome> items=null;
  		if (index!=null){
  			items = index.query(spec.withProjectionExpression("#show_col"));
  		}else {
  			items=table.query(spec.withProjectionExpression("#sk_col"));	
  		}
  		Iterator<Item> iterator = items.iterator();
  		Item item1 = null;
  		while (iterator.hasNext()) {
  		    item1 = iterator.next();
  		    String itemJSON=item1.toJSON();
  		    JsonReader reader=Json.createReader(new StringReader(itemJSON));
  		    output.add(reader.readObject());
  		}
  		return output.build();
   	}
   	private JsonArray getPartialData(String type,String brand,String input,int limit){
   		JsonArrayBuilder output=Json.createArrayBuilder();
   		DynamoDB _dynamoDB = new DynamoDB(dynamoDB);
   		Table table = _dynamoDB.getTable(hardwareTable);
   		Index index=null;
   		if (brand!=""){
	   		index= table.getIndex("Type-Brand-index");
   		}
   		Map<String,Object> vm= new ValueMap().withString(":v_id", type);
   	//	if (brand!=""){
   	//	vm.put(":sk_id", brand);
  	//	}
   		if(input!="") {
   			vm.put(":sk_begin", input);
   		}
   		Map<String, String> nm= new NameMap();
   		nm.put("#pk_col","Type");
   		if (brand!=""){
   		nm.put("#sk_col","Brand");
  		}else {
  		nm.put("#sk_col", "Name");
  		}
  		
  		String kce="#pk_col=:v_id";
   		//if (brand!=""){
  		//	kce+=" AND #sk_col =:sk_id";
  		//}
  		if(input!="") {
  			kce+=" AND begins_with(#sk_col,:sk_begin)";
  		}
  		QuerySpec spec = new QuerySpec()
  		    .withKeyConditionExpression(kce)
  		    .withNameMap(nm)
  		    .withValueMap(vm);
  		if (limit!=0) {
  			spec=spec.withMaxResultSize(limit);
  		}
  		ItemCollection<QueryOutcome> items=null;
  		if (index!=null){
  			items = index.query(spec);
  		}else {
  			items=table.query(spec.withProjectionExpression("#pk_col, #sk_col"));	
  		}
  		Iterator<Item> iterator = items.iterator();
  		Item item1 = null;
  		while (iterator.hasNext()) {
  		    item1 = iterator.next();
  		    String itemJSON=item1.toJSON();
  		    JsonReader reader=Json.createReader(new StringReader(itemJSON));
  		    output.add(reader.readObject());
  		}
  		return output.build();
   	}
	/**
	 * Simply selects the home view to render by returning its name.
	 */
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home() {
		return "home";
	}
	@CrossOrigin(origins="*")
	@RequestMapping(value = "/CPU/{Brand}", method = RequestMethod.GET,produces="application/json")
	public String getAllCPUByName(@PathVariable("Brand") String brand) {
		JsonArray result= getAllData("CPU-Config",brand);
		return result==null?null:result.toString();
	}
	@CrossOrigin(origins="*")
	@RequestMapping(value = "/GPU/{Brand}", method = RequestMethod.GET,produces="application/json")
	public String getAllGPUByName(@PathVariable("Brand") String brand) {
		JsonArray result= getAllData("GPU-Config",brand);
		return result==null?null:result.toString();
	}
	@CrossOrigin(origins="*")
	@RequestMapping(value = "/Game", method = RequestMethod.GET,produces="application/json")
	public String getAllGame() {
		JsonArray result= getAllData("Game-Info");
		return result==null?null:result.toString();
	}
	@CrossOrigin(origins="*")
	@RequestMapping(value = "/Game/Partial", method = RequestMethod.GET,produces="application/json")
	public String getPartialGame(String input,int limit) {
		JsonArray result= getPartialData("Game-Info","",input,limit);
		return result==null?null:result.toString();
	}
	/*
	@RequestMapping(value = "/Predict", method = RequestMethod.GET,produces="application/json")
	public String getPredictResult(String cpu,String gpu,String game,int resWidth,int resHeight,String setting, int ram) {
		try{
			//Process p = Runtime.getRuntime().exec("python FYP-predictFPS2.py -a \"Core i3-3240\" -b \"GeForce GTX 950 2GB\" -c \"For Honor\" -d 1920 -e 1080 -f \"Ultra\" -g 8");
			Process p=runtime.exec("ABC");
			BufferedReader stdInput = new BufferedReader(new 
	        InputStreamReader(p.getInputStream()));
	        // read the output from the command
			String s=null;
	        System.out.println("Here is the standard output of the command:\n");
	        while ((s = stdInput.readLine()) != null) {
	            System.out.println(s);
	        }
		}catch (Exception ex) {
			ex.printStackTrace();
		}
	    return "";
	    
	}
	*/
}
