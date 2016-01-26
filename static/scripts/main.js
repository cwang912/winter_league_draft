// $(document).ready(function(){
//    var $form = $('form');
//    $form.submit(function(){
//       $.post($(this).attr('action'), $(this).serialize(), function(response){
//             // do something here on success
//       },'json');
//       return false;
//    });
// });

//
// $(document).ready(function() {
//     $('#avail-players').DataTable({
//       "paging":   false,
//       "aaSorting": [1,'desc']
//     });
//     $('#draft-order').DataTable({
//       "paging":   false,
//       'searching': false,
//       'info': false
//       {{ '{% if logic == "pre" %}' }}
//         ,"aaSorting": [1,'desc']
//       {{ '{% endif %}' }}
//     });
//   }
// );

// $(document).ready(function()
//     {
//         $("#avail-players").tablesorter();
//         console.log('yes')
//     }
// );

// $('.hideme').hide();
//
// // Submit post on submit
// $(function() {
//   var submit_form = function(e) {
//       selected_team = $('select[name=select_team]').val();
//       // var x1 = '#awer'
//       // var x2 = 10.toString()
//       // console.log(concat('#awer',10.toString()));
//       // $('.team2').hide()
//       $('.hideme').hide();
//       $('.team'+selected_team).show();
//       console.log(selected_team);
//     // });
//     // return false;
//   };
//   $('#post-form').on('change', submit_form);
// });

// showOne(1);​
// $(function() {
//   var submit_form = function(e) {
//     $.getJSON($SCRIPT_ROOT + '/get_team', {
//       selected_team: $('select[name=select_team]').val(),
//     }, function(data) {
//       $('#result').hide()
//     });
//     return false;
//   };
//   $('#post-form').on('change', submit_form);
// });

// var x1 = '#awer'
// var x2 = 10.toString()
// console.log(concat('#awer',10.toString()));
//
//
// $('#post-form').on('change', function(event){
//     event.preventDefault();
//     show_team = $('select[name=select_team]').val();
//
//     console.log($('select[name=select_team]').val());
//     console.log($(this).val())  // sanity check
//     get_team();
// });
//
//
// // AJAX for posting
// function get_team() {
//     console.log("create post is working!") // sanity check
//     $.ajax({
//         url : "get_team/", // the endpoint
//         type : "POST", // http method
//         data : { the_team : $('#post-text').val() }, // data sent with the post request
//
//         // handle a successful response
//         success : function(json) {
//
//             $('#post-text').val(''); // remove the value from the input
//             console.log(json); // log the returned json to the console
//             console.log("success"); // another sanity check
//         },
//
//         error : function(xhr,errmsg,err) {
//             $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
//                 " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
//             console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//         }
//     });
// };
//
//
// function create_post() {
//     console.log("create post is working!") // sanity check
//     console.log($('#post-text').val())
// };
var CCOUNT;
$(document).ready(function () {
        CCOUNT = 120;

});
var t, count;

function cddisplay() {
    document.getElementById('timespan').innerHTML = count;
}

minutes = 2;
count = 0;

function countdown() {
    // starts countdown
    cddisplay();
    if (minutes===0) {
    } else if (count === 0) {
        count = 60;
        minutes--;
    } else {
        count--;
        t = setTimeout(countdown, 1000);
        console.log(count)
    }
}

function cdpause() {
    // pauses countdown
    clearTimeout(t);
}

function cdreset() {
    // resets countdown
    cdpause();
    minutes = 2;
    count = 0;
    cddisplay();
}




// 
// function($) {
// /*
//  * Function: fnGetColumnData
//  * Purpose:  Return an array of table values from a particular column.
//  * Returns:  array string: 1d data array
//  * Inputs:   object:oSettings - dataTable settings object. This is always the last argument past to the function
//  *           int:iColumn - the id of the column to extract the data from
//  *           bool:bUnique - optional - if set to false duplicated values are not filtered out
//  *           bool:bFiltered - optional - if set to false all the table data is used (not only the filtered)
//  *           bool:bIgnoreEmpty - optional - if set to false empty values are not filtered from the result array
//  * Author:   Benedikt Forchhammer <b.forchhammer /AT\ mind2.de>
//  */
// $.fn.dataTableExt.oApi.fnGetColumnData = function ( oSettings, iColumn, bUnique, bFiltered, bIgnoreEmpty ) {
//     // check that we have a column id
//     if ( typeof iColumn == "undefined" ) return new Array();
//
//     // by default we only want unique data
//     if ( typeof bUnique == "undefined" ) bUnique = true;
//
//     // by default we do want to only look at filtered data
//     if ( typeof bFiltered == "undefined" ) bFiltered = true;
//
//     // by default we do not want to include empty values
//     if ( typeof bIgnoreEmpty == "undefined" ) bIgnoreEmpty = true;
//
//     // list of rows which we're going to loop through
//     var aiRows;
//
//     // use only filtered rows
//     if (bFiltered == true) aiRows = oSettings.aiDisplay;
//     // use all rows
//     else aiRows = oSettings.aiDisplayMaster; // all row numbers
//
//     // set up data array
//     var asResultData = new Array();
//
//     for (var i=0,c=aiRows.length; i<c; i++) {
//         iRow = aiRows[i];
//         var aData = this.fnGetData(iRow);
//         var sValue = aData[iColumn];
//
//         // ignore empty values?
//         if (bIgnoreEmpty == true && sValue.length == 0) continue;
//
//         // ignore unique values?
//         else if (bUnique == true && jQuery.inArray(sValue, asResultData) > -1) continue;
//
//         // else push the value onto the result data array
//         else asResultData.push(sValue);
//     }
//
//     return asResultData;
// }}(jQuery));
