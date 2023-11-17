document.addEventListener('DOMContentLoaded', function () {
    var table = document.querySelector('table');
    var rows = Array.from(table.querySelectorAll('tbody > tr'));
    var headers = Array.from(table.querySelectorAll('.sortable'));

    headers.forEach(function (header) {
        header.addEventListener('click', function () {
            const children = header.childNodes;
            for (const child of children) {
                if (child.classList) {
                    if (child.classList.contains("svg")) {
                        if (child.classList.contains("rotate")) {
                            child.classList.remove('rotate');
            
                            var index = Array.from(this.parentNode.children).indexOf(this);
            
                            if (index !== 0) { // Check if the column is not the fixed column
                                rows.sort(function (a, b) {
                                    var aValue = a.querySelectorAll('td')[index].textContent;
                                    var bValue = b.querySelectorAll('td')[index].textContent;
                                    return aValue.localeCompare(bValue);
                                });
            
                                rows.forEach(function (row, i) {
                                    // Update the numbering of the first column after sorting
                                    row.querySelector('td:first-child').textContent = i + 1;
                                    table.querySelector('tbody').appendChild(row);
                                });
                            }
                        } else {
                            child.classList.add('rotate');
            
                            var index = Array.from(this.parentNode.children).indexOf(this);
            
                            if (index !== 0) { // Check if the column is not the fixed column
                                rows.sort(function (a, b) {
                                    var aValue = a.querySelectorAll('td')[index].textContent;
                                    var bValue = b.querySelectorAll('td')[index].textContent;
                                    return bValue.localeCompare(aValue);
                                });
            
                                rows.forEach(function (row, i) {
                                    // Update the numbering of the first column after sorting
                                    row.querySelector('td:first-child').textContent = i + 1;
                                    table.querySelector('tbody').appendChild(row);
                                });
                            }
                        }
                    }
                }
            }
            
        });
    });

    headers[1].click(); //time

});
