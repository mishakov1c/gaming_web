$(document).ready(function(){

    $(',btn').click(function(){
        $.ajax({
            url: '',
            type: 'get',
            contentType: 'application/jason',
            data: {
                button_text: $(this).text()
            },
            success: function(response){
                $('.btn').text(response.seconds)
            }
        })
    })
})