

$(document).ready(function(){

    // code to read selected table row cell data (values).
    $("#myTable").on('click','button.btn.btn-primary',function(){
         // get the current row

         let currentRow=$(this).closest("tr");
         let col1 = currentRow.find("td:eq(0)").text(); // get current row 1st TD value

         let ids = {
            user_id: col1
        };

        $.ajax({
            url: '/index',
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json',
            data: JSON.stringify(ids),
            type: 'POST',

            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });

    });

});





