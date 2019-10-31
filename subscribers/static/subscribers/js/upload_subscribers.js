$(document).ready(function()
{

  $('#file').change(function()
  {
      if ($(this).val()) 
        $('#uploadButton').prop('disabled', false);
       
  });

  $('#importButton').click(function()
  {
    $('#formUpload').show();
    $('#button-close-results').hide();
    $('#upload-results').html('');
    $('#uploadButton').html('Upload');
    $("#file").val(null);
    $('#uploadButton').prop('disabled', true);


  });

  $('#uploadButton').click(function(){

    // disable button
      $(this).prop("disabled", true);
      // add spinner to button
      $(this).html( $("#spinner-upload").html());

    var fd = new FormData();
    var files = $('#file')[0].files[0];
    fd.append('file',files);


    // AJAX request
    $.ajax({
      url: $( "#url_upload_csv" ).text(),
      type: 'post',
      headers: { "X-CSRFToken": $( "input[name=csrfmiddlewaretoken]" ).val() },
      data: fd,
      contentType: false,
      processData: false,
      success: function(response){
        $('#formUpload').hide();
        $('#button-close-results').show();
        
        if(response != 0){          
          $('#upload-results').html(response);          
        }else{
          $('#upload-results').html("Conection ERROR"); 
        }
      }
    });
  });
});

