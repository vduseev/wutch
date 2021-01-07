function wutch() {
  while (true) {
    fetch("http://localhost:50231")
      .then(response => response.json())
      .then(response => {
        if (response.status == "changed") {
          window.location.reload();
        }
      });
    sleep(1);
  }
}
