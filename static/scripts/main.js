// $(document).ready(function(){
//    var $form = $('form');
//    $form.submit(function(){
//       $.post($(this).attr('action'), $(this).serialize(), function(response){
//             // do something here on success
//       },'json');
//       return false;
//    });
// });

$('.hideme').hide();

// Submit post on submit
$(function() {
  var submit_form = function(e) {
      selected_team = $('select[name=select_team]').val();
      // var x1 = '#awer'
      // var x2 = 10.toString()
      // console.log(concat('#awer',10.toString()));
      // $('.team2').hide()
      $('.hideme').hide();
      $('.team'+selected_team).show();
    // });
    // return false;
  };
  $('#post-form').on('change', submit_form);
});

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
