$(document).ready(function() {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

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
        var data = {'outbound': outbound, 'inbound': inbound};
        var checkRoundTrip = $('.inbound').is(':checked') || ($('.inbound').length == 0 && $.isEmptyObject(inbound));
        if ($('.outbound').is(':checked') && checkRoundTrip ) {
            $.ajax({
                type: 'POST',
                url: '/flights/select/',
                contentType: "application/json",
                data: JSON.stringify(data),
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },

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
            alert('Please select your flight')
        }
    });

    $('.pay-schedule').change(function(){
        $('.pay-schedule').not(this).prop('checked', false);
        var paySoonNotification = $('#pay-soon');
        if ($(this).attr('id') === 'pay-now') {
            paySoonNotification.hide();
        } else {
            paySoonNotification.show();
        }
    });

    $('#confirm-pay-schedule').click(function(){
        var paySchedule = $('.pay-schedule:checked').attr('id');
        var data = {'pay_schedule': paySchedule};
        if ($('#agree-to-terms').is(':checked')){
            $.ajax({
                type: 'POST',
                url: '/bookings/summary/',
                contentType: "application/json",
                data: JSON.stringify(data),
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },

                success: function (data, status) {
                    if (status === 'success') {
                        console.log('Successful', data);
                        location.href = '/bookings/process_booking'
                    } else {
                        alert('Something went wrong')
                    }
                },

                error: function (error) {
                    if (error) {
                        console.log('Error', error);
                    }
                }
            })
        } else {
            alert('Please click the checkbox to accept our terms and condition')
        }
    });

});