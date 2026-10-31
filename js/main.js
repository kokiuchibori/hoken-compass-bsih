(function () {
  var data = window.SITE_DATA || { services: [] };

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // 広告リンクには rel="sponsored" を付ける（Google のガイドライン準拠）
  function ctaLink(item, label) {
    return '<a class="btn btn-cta" href="' + esc(item.affiliateUrl) +
      '" target="_blank" rel="sponsored noopener">' + esc(label) + "</a>";
  }

  // サービス一覧
  var list = document.getElementById("service-list");
  if (list) {
    list.innerHTML = data.services.map(function (s, i) {
      return '<div class="rank-item">' +
        '<div class="rank-head"><div class="rank-no">' + (i + 1) + "</div><h3>" + esc(s.name) + "</h3></div>" +
        "<div>" + s.tags.map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("") + "</div>" +
        "<ul>" + s.points.map(function (p) { return "<li>" + esc(p) + "</li>"; }).join("") + "</ul>" +
        ctaLink(s, "公式サイトで詳細を見る") +
        "</div>";
    }).join("");
  }

  // 比較表
  var table = document.getElementById("service-table");
  if (table) {
    var rows = [
      ["相談方法", "style"],
      ["取扱保険会社数", "companies"],
      ["担当者変更", "change"],
      ["対応地域", "area"]
    ];
    var html = "<thead><tr><th></th>" +
      data.services.map(function (s) { return "<th>" + esc(s.name) + "</th>"; }).join("") +
      "</tr></thead><tbody>";
    rows.forEach(function (r) {
      html += "<tr><th>" + r[0] + "</th>" +
        data.services.map(function (s) { return "<td>" + esc(s[r[1]]) + "</td>"; }).join("") + "</tr>";
    });
    html += "<tr><th>公式サイト</th>" +
      data.services.map(function (s) { return "<td>" + ctaLink(s, "詳細") + "</td>"; }).join("") +
      "</tr></tbody>";
    table.innerHTML = html;
  }

  document.querySelectorAll("[data-checked-at]").forEach(function (el) {
    el.textContent = data.checkedAt;
  });

  // 必要保障額シミュレーター（死亡保障）
  // 必要保障額 = 遺族に必要な支出 −（遺族の収入見込み ＋ 準備済みの資産）
  var form = document.getElementById("sim-form");
  if (form) {
    var man = function (n) { return Math.round(n).toLocaleString("ja-JP") + "万円"; };
    var v = function (name) { return Math.max(0, Number(form[name].value) || 0); };
    var calc = function () {
      var years = v("years");
      var need = v("living") * 12 * years + v("education") + v("housing") + v("funeral");
      var have = v("pension") * 12 * years + v("income") * years + v("savings") + v("retirement");
      var gap = need - have;

      document.getElementById("res-need").textContent = man(need);
      document.getElementById("res-have").textContent = man(have);
      document.getElementById("res-gap").textContent = gap > 0 ? man(gap) : "0万円";
      var p = need > 0 ? Math.min(100, (have / need) * 100) : 100;
      document.querySelector(".bar .principal").style.width = p + "%";
      document.querySelector(".bar .gain").style.width = (100 - p) + "%";
      document.getElementById("res-comment").textContent = gap > 0
        ? "※入力した条件では、公的保障と貯蓄だけでは約" + man(gap) + "不足する計算です。この不足分が民間保険で備える目安になります。"
        : "※入力した条件では、公的保障と貯蓄で必要額をまかなえる計算です。死亡保障を増やす必要は小さいかもしれません。";
    };
    form.addEventListener("input", calc);
    calc();
  }
})();
