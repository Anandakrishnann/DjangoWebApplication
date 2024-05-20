function confirmDelete(userId) {
    if (confirm("Are you sure you want to delete this user?")) {
        document.getElementById('delete-form-' + userId).submit();
    }
}