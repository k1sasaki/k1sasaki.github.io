// 本番(k1sasaki.github.io)以外で開いたときだけ、タブのタイトルに目印を付ける
if (location.hostname !== "k1sasaki.github.io") {
  document.title = "🔧 " + document.title;
}
