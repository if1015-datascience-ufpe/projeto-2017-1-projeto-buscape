var main_data = [];
var filters = {};
var currentData = null;

var chart = null;
var materialOptions = {
      title : 'Price x Feature',
      vAxis: {title: 'Feature'},
      hAxis: {title: 'Cost (R$)'},
      seriesType: 'bars',
      series: {1: {type: 'line'}},
      orientation: 'vertical'
    };	
$(document).ready(function(){
	$("#main").hide();
	google.charts.load('current', {packages: ['corechart']});
	google.charts.setOnLoadCallback(buildChart);
	
	$.ajax(
        {
            url: "http://23.251.151.44:5000/categories",//"/test/server/categories.php",//
            /*beforeSend: function(request) {
                request.setRequestHeader("Access-Control-Allow-Origin", "*");
            },*/
            headers: { "Access-Control-Allow-Origin": "*", "Content-type": "application/json"},
            error:function( jqXHR, textStatus, errorThrown ){
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            },
            crossDomain: true,
            success: function(result){
            	main_data = JSON.parse(result)
                onLoadMainData();
                }
            });

	$("#btn-feature").click(onSelectFeature);
	$(".filter").on("click",".badge",onRemoveFilter);
});

function onLoadMainData(){
	for(var i=0;i<main_data.length;i++){
		if(main_data[i].name != "url"){
			$("#feature").append("<option value='"+main_data[i].id+"'>"+main_data[i].name+"</option>");
		}
	}
	$("#main").show();
	$("#loading").hide();
}

function addFilter(feature,group_id){
	filters[feature] = parseInt(group_id);
	var feat_data = getFeatureData(feature);
	var name = feat_data.name;
	name = name +": "+getGroupByID(feat_data.groups, group_id);
	addFilterDiv(name,feature);
	
}
function addFilterDiv(text, feature){
	var li = "<li class=\"list-group-item\"><span class=\"badge\" feature=\""+feature+"\">x</span>"+text+"</li>";
	$(".filter").append(li);
	$("#feature").val("");
}

function getGroupByID(groups, group_id){
	for(var key in groups){
		if(groups[key] == group_id){
			return key;
		}
	}
	return null;
}

function removeFilter(feature){
	delete filters[feature];
	onSelectFeature();
}

function onSelectFeature(){
	var feature_id = $("#feature").val();
	var param = {};
	param.category = parseInt(feature_id);

	param.filters = filters;
	param = JSON.stringify(param);
	$.ajax(
        {
        	method:"POST",
        	data: param,
            url: "http://23.251.151.44:5000/analyse",//"/test/server/analyse.php",//
            /*beforeSend: function(request) {
                request.setRequestHeader("Access-Control-Allow-Origin", "*");
            },*/
            headers: { "Access-Control-Allow-Origin": "*", "Content-type": "application/json"},
            error:function( jqXHR, textStatus, errorThrown ){
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            },
            crossDomain: true,
            success: function(result){
            	rst = JSON.parse(result);
                onAnalysisSucceed(rst);
                }
            });
}

function onAnalysisSucceed(rst){
	var feature_data = getFeatureData($("#feature").val());
	
	var arr = [];
	arr[arr.length] = [feature_data.name, 'Price','Base Price'];
	
	var base_price = rst.intercept;

	currentData = rst.coefs_indexes;
	
	for(var i=0;i<rst.coefs.length;i++){

		arr[arr.length] = [ getGroupByID(feature_data.groups, currentData[i]), base_price + rst.coefs[i], base_price];	
	}



	var data = google.visualization.arrayToDataTable(arr);

	materialOptions["title"] = feature_data.name+" vs Price";
	materialOptions["vAxis"]["title"] = feature_data.name;
	
	chart.draw(data, materialOptions);

}

function getFeatureData(id){
	for(var i=0;i<main_data.length;i++){
		if(main_data[i].id == id){
			return main_data[i];
		}
	}
	return null;
}

function onRemoveFilter(){
	var feat = $(this).attr("feature");
	$(this).closest(".list-group-item").remove();
	removeFilter(feat);
}

function buildChart(){
	chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
	google.visualization.events.addListener(chart, 'select', selectHandler);
}
function selectHandler() {
    var selectedItem = chart.getSelection()[0];
    if (selectedItem) {
    	addFilter($("#feature").val(), currentData[selectedItem.row]);
    }
  }