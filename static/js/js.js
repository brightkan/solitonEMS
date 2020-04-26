$(document).ready(() => {
    $("#leave_type").change(() => {
        leave_type = document.querySelector('#leave_type').value;

        $.ajax({
            type: 'get',
            url: configuration['leave']['get_no_of_days'],
            data: { 'leave_type': leave_type },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#no_days').value = data.no_of_days;
                    if (data.leave == "Annual") {
                        document.querySelector('#no_days').readOnly = false;
                    } else {
                        document.querySelector('#no_days').readOnly = true;
                    }
                } else {
                    alert(data.message);
                }

            },

        });
    });

    $("#no_days").blur(() => {
        leave_type = document.querySelector('#leave_type').value;

        $.ajax({
            type: 'get',
            url: configuration['leave']['get_no_of_days'],
            data: { 'leave_type': leave_type },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#no_days').value = data.no_of_days;
                    if (data.leave == "Annual") {
                        document.querySelector('#no_days').readOnly = false;
                    } else {
                        document.querySelector('#no_days').readOnly = true;
                    }
                } else {
                    alert(data.message);
                }

            },

        });
    });

    $("#st_date").change(() => {
        start_date = document.querySelector('#st_date').value;
        no_days = document.querySelector('#no_days').value;

        $.ajax({
            type: 'get',
            url: configuration['leave']['get_end_date'],
            data: { 'startDate': start_date, 'no_of_days': no_days },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#end_date').value = data.end_date;
                } else {
                    //alert(data.message);
                }

            },

        });
    });

    $('.table tbody').on('click', '.fa fa-edit', () => {
        var row = $(this).closest('tr');

        document.querySelector('#edit_type').value = row.find('td:eq(1)').text();
        // document.querySelector('#edit_days').value = row.find('td:eq(1)').text();
        // document.querySelector('#edit_desc').value = row.find('td:eq(2)').text();

        var cc = row.find('td:eq(1)').text();
        console.log(cc);
        alert(cc);
    });
});