$(function () {
    $.get(orderListApiUrl, function (response) {
        if (response) {
            var table = '';
            var totalCost = 0;
            $.each(response, function (index, order) {
                totalCost += parseFloat(order.total);
                table += '<tr>' +
                    '<td>' + order.datetime + '</td>' +
                    '<td>' + order.order_id + '</td>' +
                    '<td>' + order.customer_name + '</td>' +
                    '<td>' + parseFloat(order.total).toFixed(2) + ' Rs</td></tr>';
            });
            table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>' + totalCost.toFixed(2) + ' Rs</b></td></tr>';
            $('table').find('tbody').empty().html(table);
        }
    });

    $.get('http://127.0.0.1:5000/getDashboardSummary', function (summary) {
        if (summary) {
            $('#stat-orders').text(summary.order_count || 0);
            $('#stat-products').text(summary.product_count || 0);
            $('#stat-revenue').text((summary.revenue || 0).toFixed(2) + ' Rs');
        }
    });
});