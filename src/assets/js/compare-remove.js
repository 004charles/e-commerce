/**=====================
   Compare Remove JS
==========================**/
document.querySelector('.compare-table').addEventListener('click', function (event) {
    if (event.target.classList.contains('remove_column')) {
        var ndx = event.target.parentNode.cellIndex + 1;
        var table = event.delegateTarget;
        var headers = table.querySelectorAll('th');
        var cells = table.querySelectorAll('td');

        headers[ndx - 1].remove();
        for (var i = 0; i < cells.length; i++) {
            if ((i + 1) % headers.length === ndx) {
                cells[i].remove();
            }
        }
    }
});