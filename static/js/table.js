let i = 0;

setTimeout(function () {
  let id_table = $("th#row");

  for (let i = 0; i < id_table.length; i++) {
    $(document).ready(function () {
      let id = $("th#row");

      id[i].innerText = i + 1;
    });
  }
}, 200);
