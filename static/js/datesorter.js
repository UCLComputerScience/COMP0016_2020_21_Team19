function dateSorter(a, b) {
    a = a.replace(/<\/?small[^>]*>/g, '').replace(/\s+/g,' ');
    b = b.replace(/<\/?small[^>]*>/g, '').replace(/\s+/g,' ');
    return Date.parse(a) - Date.parse(b);
}