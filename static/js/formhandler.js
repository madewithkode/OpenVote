$(document).ready(function() {
    $('#verify-admin').submit(function (e) {
     //change button to loading gif
      var url = "{{ url_for('verifyAdmin') }}";
      $.ajax({
        type: "POST",
        url: url,
        data: $('#verify-admin').serialize(),
        success: function (data) {
          window.location.href(data)
    }
    
      
    });
    e.preventDefault();
    });

    $.ajaxSetup({
    beforeSend: function(xhr, settings){
    if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', '{{ #verify-admin.csrf_token._value()}}')
    }
    }
    })
});