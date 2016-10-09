/*
 Copyright (c) 2016 Sebastian Kanis
 This file is part of pi-led-control.

 pi-led-control is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pi-led-control is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with pi-led-control.  If not, see <http://www.gnu.org/licenses/>.
*/
var startProgramURL = "/startProgram";
var setBrightnessURL = "/setBrightness";
var configureProgramURL = "configureProgram";
var currentBrightness = 1;


//check if variable is int
function isInteger(x) {
    return parseInt(x, 10) == x;
}

//check if variable is float
function isFloat(x) {
    return !isNaN(parseFloat(x));
}

//check if variable is time of format HH:MM:SS
function isValidTime(x){
    if(x.length != 8){
	return false;
    }
    var hours = x.substring(0,2);
    var minutes = x.substring(3,5);
    var seconds = x.substring(6,7);
    if(!isInteger(hours) || !isInteger(minutes) || !isInteger(seconds)){
	return false;
    }
    if(hours < 0 || hours > 23){
	return false;
    }
    if(minutes < 0 || minutes > 59){
	return false;
    }
    if(seconds < 0 || seconds > 59){
	return false;
    }
    return true;
}

//update the colors in the demo area (free color) from the slider values
function updateColorFromSliders(){
    var red = $( "#redSlider").val();
    var green= $( "#greenSlider").val();
    var blue= $( "#blueSlider").val();
    var brightness= $( "#freeColorBrightnessSlider").val();
    $("#colorDemo").css('background-color', 'rgb(' + Math.round(parseInt(red)*parseFloat(brightness)) + ','+ Math.round(parseInt(green)*parseFloat(brightness)) + ',' + Math.round(parseInt(blue)*parseFloat(brightness)) + ')');
    $("#colorDemo").val("red: " + red + " green: " + green + " blue: " + blue + " brightness: " + brightness * 100 + "%");
}

function updatePredefinedColorDemo(){
    var red = $( "#editPredefinedRedSlider").val();
    var green= $( "#editPredefinedGreenSlider").val();
    var blue= $( "#editPredefinedBlueSlider").val();
    var brightness= 1.0;
    $("#editPredefinedColorDemo").css('background-color', 'rgb(' + Math.round(parseInt(red)*parseFloat(brightness)) + ','+ Math.round(parseInt(green)*parseFloat(brightness)) + ',' + Math.round(parseInt(blue)*parseFloat(brightness)) + ')');
    $("#editPredefinedColorDemo").text("red: " + red + " green: " + green + " blue: " + blue + " brightness: " + brightness * 100 + "%");
}   

/*frequently update the status from the server
  the status currently contains the current color and if a (power) off is scheduled
*/
function updateStatus(){
    $.getJSON( "/getStatus", function( data ) {
	var colors = data.color;
	if(colors !== null){
	    var red = Math.round(colors.red*255.0*data.brightness);
	    var green = Math.round(colors.green*255.0*data.brightness);
	    var blue = Math.round(colors.blue*255.0*data.brightness);
	    
	    $("#currentColor").css('background-color', 'rgb('+ red +','+ green + ','+ blue + ')');
	    $("#currentColor").val("");
	}else{
	    $("#currentColor").css('background-color', '#FFFFFF');
	    $("#currentColor").val("NA");
	}
	if(data.powerOffScheduled){
	    $( "#cancelscheduledOff-button" ).show();
	    $( "#scheduleOff-button" ).hide();
	}else{
	    $( "#cancelscheduledOff-button" ).hide();
	    $( "#scheduleOff-button" ).show();
	}
	$("#currentBrightness").text(Math.round(data.brightness*100) + "%");
    }).error(function() {
    });
    setTimeout(updateStatus, 500);
}

//converts a time of day to seconds in current day
function timeToSecondsOfDay(x){
    return parseInt(x.substring(0,2)) * 3600 + parseInt(x.substring(3,5)) * 60 + parseInt(x.substring(6,8));
}

//converts seconds to time of day in current day
function secondsOfDayToTime(x){
    var hours = Math.floor(x/3600);
    var minutes = Math.floor(x-3600*hours);
    var seconds = Math.floor(x-3600*hours-60*minutes);
    if(hours < 10){
	hours = "0" + hours;
    }
    if(minutes < 10){
	minutes = "0" + minutes;
    }
    if(seconds < 10){
	seconds = "0" + seconds;
    }
    return hours + ":" + minutes + ":" + seconds;
}


function initEditPredefinedModal(oldColorName, red, green, blue){
    $("#editPredefinedColorName").val(oldColorName);
    $("#editPredefinedRedSlider").val(red);
    $("#editPredefinedGreenSlider").val(green);
    $("#editPredefinedBlueSlider").val(blue);
    updatePredefinedColorDemo();
    $("#editPredefinedPreview-button").on('click', function(){
       var redValue = $( "#editPredefinedRedSlider").val();
	   var greenValue = $( "#editPredefinedGreenSlider").val();
	   var blueValue = $( "#editPredefinedBlueSlider").val();
	   $.post( startProgramURL, JSON.stringify({name: "single", params: {red: redValue, green: greenValue, blue: blueValue} }) );
	   $.post( setBrightnessURL, JSON.stringify({params: {brightness: 1.0} }));	
    });
    //remove all existing listeners
    var el = document.getElementById('savePredefinedColor-button'),
    elClone = el.cloneNode(true);
    el.parentNode.replaceChild(elClone, el);
    //TODO add errorhandling
    $("#savePredefinedColor-button").on('click', function(){
       var colorName = $("#editPredefinedColorName").val();
       var redValue = $( "#editPredefinedRedSlider").val();
       var greenValue = $( "#editPredefinedGreenSlider").val();
       var blueValue = $( "#editPredefinedBlueSlider").val();
       var jsonBody = JSON.stringify({params: {oldName: oldColorName, name: colorName, red: redValue, green: greenValue, blue: blueValue} });
       $.post( "/configureColor", jsonBody);
       updateConfiguration();
    });
    $("#editPredefinedColorModal").modal('show');
}

function updatePredefinedColors(colors){
    $("#predefinedColor-button-group").empty();
    $("#configurePredefinedColor-body").empty();
    $("#configureColorLoop-body").empty();
    $.each(colors, function(key,value){
	var name = value.name;
	var red = Math.round(value.values.red*255);
	var green = Math.round(value.values.green*255);
	var blue = Math.round(value.values.blue*255);
	
	
	$("#predefinedColor-button-group").append("<li><button type='button' class='btn btn-block' id='" + name + "-button' style='background-color: rgb("+ red +","+ green + ","+ blue + ")'>" + name + "</button></li>");
	$("#" + value.name + "-button").on('click', function(){
	    var body = JSON.stringify({name: "predefined", params: {colorName: value.name} });
	    $.post( startProgramURL, body);});
  
	$("#configurePredefinedColor-body").append(
	   /*jshint multistr: true */
	    "<div class='row' style='padding:2px'>\
                <div class='col-xs-6 col-md-6 list-btn-col vcenter'>\
                   <button type='button' class='btn btn-block' id='activate" + name + "-button' style='background-color: rgb("+ red +","+ green + ","+ blue + ")'>" + name + "</button>\
                </div>\
	        <div class='col-xs-3 col-md-3 list-btn-col'>\
		   <button type='button' class='btn btn-block btn-default' id='edit-" + name + "-button'>Edit</button>\
	        </div>\
	        <div class='col-xs-3 col-md-3 config-btn-col'>\
		   <button type='button' class='btn btn-block btn-default' id='delete-" + name + "-button'>Delete</span></button>\
	        </div>\
            <div>");
	$("#activate" + name + "-button").on('click', function(){
	    $.post( startProgramURL, JSON.stringify({name: "predefined", params: {colorName: name} }));});
	$("#edit-" + name + "-button").on('click', function(){
	    name = value.name;
	    red = Math.round(value.values.red*255);
	    green = Math.round(value.values.green*255);
	    blue = Math.round(value.values.blue*255);
	    initEditPredefinedModal(name, red, green, blue);
	});
	$("#delete-" + name + "-button").on('click', function(){
	   $.post( "/deleteColor", JSON.stringify({params: {name: name} }));
	   updateConfiguration();
	});
	$("#configureColorLoop-body").append(
       /*jshint multistr: true */
        "<div class='row' style='padding:2px'>\
                <div class='col-xs-12 col-md-12 list-btn-col vcenter' style='text-align: center;'>\
                    <input id='configureColorLoop-" + name + "-toggle' data-toggle='toggle' type='checkbox' data-on='" + name + "' data-off='" + name + "'data-style='" + name +"'>\
                </div>\
           <div>");   
        $("#configureColorLoop-" + name + "-toggle").bootstrapToggle();
        $("#configureColorLoop-" + name + "-toggle").parent().css('min-width', '50%');
        $("#configureColorLoop-" + name + "-toggle").next().children(":first").css('color', 'rgb(' + red + ','+ green + ','+ blue + '');
    });
}

function updateConfiguration(){
    $.getJSON("/getConfiguration", function( data ){
	$("#timePerColor").val(data.programs.randomPath.timePerColor);
	$("#feedBrightnessSlider").val(data.programs.feed.brightness);
	$("#freakSecondsPerColor").val(data.programs.freak.secondsPerColor);
	$("#wheelSecondsPerColor").val(data.programs.wheel.timePerColor);
	$("#wheelMinBrightnessSlider").val(data.programs.wheel.minBrightness);
    $("#wheelMaxBrightnessSlider").val(data.programs.wheel.maxBrightness);
    $("#sunriseDuration").val(data.programs.sunrise.duration);
	var timeOfDay = data.programs.sunrise.timeOfDay;
	if(timeOfDay == -1){
	    $('#sunriseStarttime').val("");
	}else{
	    $('#sunriseStarttime').val(secondsOfDayToTime(timeOfDay));
	}
	$("#sunriseBrightnessSlider").val(data.programs.sunrise.brightness);
	//update predefined colors
	updatePredefinedColors(data.userDefinedColors);
	//update colorloop colors
	$.each(data.programs.colorloop.colors, function(key,value){
	    $("#configureColorLoop-" + value + "-toggle").bootstrapToggle('on');
	});
    });
}

$(document).ready(function() {
    //initialize the main buttons
    $( "#off-button" ).on('click', function() {
	$.post( startProgramURL, JSON.stringify({name: "off", params: [] }) );
    });
    $( "#soft-off-button" ).on('click', function() {
	$.post( startProgramURL, JSON.stringify({name: "softOff", params: [] }) );
    });
    $( "#cancelscheduledOff-button" ).hide();
    $( "#cancelscheduledOff-button" ).on('click', function() {
	$.post( startProgramURL, JSON.stringify({name: "cancelScheduledOff", params: [] }) );
    });
    $( "#white-button" ).on('click', function() {
	$.post( startProgramURL, JSON.stringify({name: "white", params: [] }) );
    });
    $( "#feed-button" ).on('click', function() {
	$.post( startProgramURL, JSON.stringify({name: "feed", params: [] }) );
    });
    $( "#4colorloop-button" ).on('click', function() {
	$.post( startProgramURL, JSON.stringify({name: "colorloop", params: [] }) );
    });
    $( "#wheel-button" ).on('click', function() {
	$.post( startProgramURL, JSON.stringify({name: "wheel", params: [] }) );
    });
    $( "#freak-button" ).on('click', function() {
	$.post( startProgramURL, JSON.stringify({name: "freak", params: [] }) );
    });
    $( "#randompath-button" ).on('click', function() {
	$.post( startProgramURL, JSON.stringify({name: "randomPath", params: [] }) );
    });

    //listener for startSunrise including input validation
    $( "#startSunrise-button" ).on('click', function() {
	var sunriseDuration = $('#sunriseDuration').val();
	var sunriseStarttime = $('#sunriseStarttime').val();
	var valid = false;
	$('#sunriseDuration').parent().append("<span class='glyphicon glyphicon-remove form-control-feedback'></span>");
	$('#sunriseStarttime').parent().append("<span class='glyphicon glyphicon-remove form-control-feedback'></span>");
	if (isInteger(sunriseDuration)){
	    $('#sunriseDuration').parent().removeClass("has-error");
	    $('#sunriseDuration').parent().removeClass("has-feedback");
	    valid = true;	    
	}else{
	    $('#sunriseDuration').parent().addClass("has-feedback");
	    $('#sunriseDuration').parent().addClass("has-error");
	}
	if(sunriseStarttime !== ""){
	    if (isValidTime(sunriseStarttime)){
		$('#sunriseStarttime').parent().removeClass("has-error");
		$('#sunriseStarttime').parent().removeClass("has-feedback");
		valid = true;	    
	    }else{
		$('#sunriseStarttime').parent().addClass("has-feedback");
		$('#sunriseStarttime').parent().addClass("has-error");
	    }
	}
	if(valid){
	    if(sunriseStarttime !== ""){
		$.post( startProgramURL, JSON.stringify({name: "sunrise", params: {duration: sunriseDuration, timeOfDay: timeToSecondsOfDay(sunriseStarttime), brightness: $('#sunriseBrightnessSlider').val()}}));
	    }else{
		$.post( startProgramURL, JSON.stringify({name: "sunrise", params: {duration: sunriseDuration, brightness: $('#sunriseBrightnessSlider').val()}}));
	    }
	    updateConfiguration();
	    $('#sunriseModal').modal('hide');
	}
    });
    //listener for scheduledOff including input validation
    $( "#scheduleOffSave-button" ).on('click', function() {
	var scheduledOffDuration = $('#scheduleOffDuration').val();
	$('#scheduledOffDuration').parent().append("<span class='glyphicon glyphicon-remove form-control-feedback'></span>");
	var valid = false;
	if (isFloat(scheduledOffDuration) || Math.isInt(scheduledOffDuration)){
	    $('#scheduleOffDuration').parent().removeClass("has-error");
	    $('#scheduleOffDuration').parent().removeClass("has-feedback");
	    valid = true;	    
	}else{
	    $('#scheduleOffDuration').parent().addClass("has-feedback");
	    $('#scheduleOffDuration').parent().addClass("has-error");
	}
	if(valid){
	    $.post( startProgramURL, JSON.stringify({name: "scheduledOff", params: {duration: scheduledOffDuration*60} }));
	    $('#scheduledOffModal').modal('hide');
	}
    });

    //listner for free color button
    $( "#freeColorSave-button" ).on('click', function() {
	var redValue = $( "#redSlider").val();
	var greenValue = $( "#greenSlider").val();
	var blueValue = $( "#blueSlider").val();
	$.post( startProgramURL, JSON.stringify({name: "single", params: {red: redValue, green: greenValue, blue: blueValue} }) );
	var brightnessValue = $( "#freeColorBrightnessSlider").val();
	$.post( setBrightnessURL, JSON.stringify({params: {brightness: brightnessValue} }));
    });
    $( "#brightnessSlider" ).change(function() {
	   var brightnessValue = $( "#brightnessSlider").val();
	$.post( setBrightnessURL, JSON.stringify({params: {brightness: brightnessValue} }));
    });

    //listeners for sliders in free color modal
    $( "#redSlider" ).change(function(){
	updateColorFromSliders();
    });
    $( "#greenSlider" ).change(function(){
	updateColorFromSliders();
    });
    $( "#blueSlider" ).change(function(){
	updateColorFromSliders();
    });
    $( "#freeColorBrightnessSlider" ).change(function(){
	updateColorFromSliders();
    });
    //listeners for sliders in edit predefined color modal
    $( "#editPredefinedRedSlider" ).change(function(){
	updatePredefinedColorDemo();
    });
    $( "#editPredefinedGreenSlider" ).change(function(){
	updatePredefinedColorDemo();
    });
    $( "#editPredefinedBlueSlider" ).change(function(){
	updatePredefinedColorDemo();
    });

    //start update of status
    updateStatus();
    //initialize the slides in free color modal from the last status when the modal is opened
    $("#freeButton").on('click', function(){
	$("#freeColorModal").modal('show');
	$.getJSON( "/getStatus", function( data ) {
	    var colors = data.color;
	    $("#redSlider").val(colors.red*255);
	    $("#greenSlider").val(colors.green*255);
	    $("#blueSlider").val(colors.blue*255);
	    $("#brightnessSlider").val(data.brightness);
	    $("#freeColorBrightnessSlider").val(data.brightness);
	    updateColorFromSliders();
	});
    });
    $("#randompath-openconfig-button").on('click', function(){
	$("#configureRandomModal").modal('show');
    });
    $( "#configureRandomPath-button" ).on('click', function() {
	$.post(configureProgramURL, JSON.stringify({name: "randomPath", params: {timePerColor: $("#timePerColor").val()} }) );
	$("#configureRandomModal").modal('hide');
	updateConfiguration();
    });

    $("#feed-openconfig-button").on('click', function(){
	$("#configureFeedModal").modal('show');
    });
    $( "#configureFeed-button" ).on('click', function() {
	$.post(configureProgramURL, JSON.stringify({name: "feed", params: {brightness: $("#feedBrightnessSlider").val()} }) );
	$("#configureFeedModal").modal('hide');
	updateConfiguration();
    });
    $("#wheel-openconfig-button").on('click', function(){
    $("#configureWheelModal").modal('show');
    });
    $("#colorloop-openconfig-button").on('click', function(){
        $("#configureColorLoopModal").modal('show');
    });
    $("#save-configureColorLoop-button").on('click', function(){
        var checkedCheckboxes = $("#configureColorLoop-body").find("input:checkbox:checked");
        var newColors = [];
        $.each(checkedCheckboxes, function(key,value){
            newColors.push($(value).attr("data-on"));
        });
        var jsonBody = JSON.stringify({name: "colorloop", params: {colors: newColors} });
        $.post( "/configureProgram", jsonBody);
        updateConfiguration();
        $("#configureColorLoopModal").modal('hide');
    });
    
    $("#configureWheel-button").on('click', function(){
        var wheelSecondsPerColor = $('#wheelSecondsPerColor').val();
        $('#wheelSecondsPerColor').parent().append("<span class='glyphicon glyphicon-remove form-control-feedback'></span>");
        var valid = false;
        if (isFloat(wheelSecondsPerColor) || Math.isInt(wheelSecondsPerColor)){
            $('#wheelSecondsPerColor').parent().removeClass("has-error");
            $('#wheelSecondsPerColor').parent().removeClass("has-feedback");
            valid = true;       
        }else{
            $('#wheelSecondsPerColor').parent().addClass("has-feedback");
            $('#wheelSecondsPerColor').parent().addClass("has-error");
        }
        if(valid){
            $.post(configureProgramURL, JSON.stringify({name: "wheel", params: {timePerColor: wheelSecondsPerColor, minValue: $('#wheelMinBrightnessSlider').val(), maxValue:$('#wheelMaxBrightnessSlider').val()} }));
            $('#configureWheelModal').modal('hide');
            updateConfiguration();
        }
    });
    $("#freak-openconfig-button").on('click', function(){
	$("#configureFreakModal").modal('show');
    });
    $( "#configureFreak-button" ).on('click', function() {
	$.post(configureProgramURL, JSON.stringify({name: "freak", params: {secondsPerColor: $("#freakSecondsPerColor").val()} }) );
	$("#configureFreakModal").modal('hide');
	updateConfiguration();
    });

    $("#predefined-openconfig-button").on('click', function(){
	$("#configurePredefinedColorModal").modal('show');
    });

    $("#add-new-predefined-button").on('click', function(){
        var name = "";
        var red = Math.round(0.5*255);
        var green = Math.round(0.5*255);
        var blue = Math.round(0.5*255);
        initEditPredefinedModal(name, red, green, blue);
    });
    
    updateConfiguration();

    $("#setBrightness-button").on('click', function(){
	$.getJSON( "/getStatus", function( data ) {
    	    $("#brightnessSlider").val(data.brightness);
	});
    });

});
