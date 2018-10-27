$(document).ready(function() {

    $('.trip-mode-label').change(function(){
        $('.trip-mode-label').not(this).prop('checked', false);
        var returnDate = $('#id_returning_date');
        if ($(this).attr('id') === 'one-way'){
            $("label[for='id_returning_date']").hide( 'slow' );
            returnDate.hide( 'slow' );
            returnDate.val('');
        } else if ($(this).attr('id') === 'round-trip') {
            $("label[for='id_returning_date']").show( 'slow' );
            returnDate.show( 'slow' );
        }
    });

    var outbound = {};
    $('.outbound').change(function(){
        $('.outbound').not(this).prop('checked', false);
        var selectedClass = $(this).attr('name');
        var selectedFlight = $(this).attr('id');
        outbound = {
            flightClass: selectedClass,
            flightId: selectedFlight
        };
    });

    var inbound = {};
    $('.inbound').change(function () {
        $('.inbound').not(this).prop('checked', false);
        var selectedClass = $(this).attr('name');
        var selectedFlight = $(this).attr('id');
        inbound = {
            flightClass: selectedClass,
            flightId: selectedFlight
        };
    });

    $('#submit-flights').click(function(){
        var tripMode = $('.trip-mode-label:checked').attr('name');
        var data = {'trip_mode': tripMode, 'outbound': outbound, 'inbound': inbound};
        console.log('Flight', data);
        if (outbound) {
            $.ajax({
                type: 'POST',
                url: '/flights/select/',
                contentType: "application/json",
                data: JSON.stringify(data),

                success: function (data, status) {
                    if (status === 'success') {
                        console.log('Data', data);
                        location.href = '/flights/review'
                    } else {
                        alert('There is something wrong with the form')
                    }
                },

                error: function (error) {
                    if (error) {
                        console.log('Error', error);
                    }
                }
            })
        } else {
            alert('Please select a flight')
        }
    });
});