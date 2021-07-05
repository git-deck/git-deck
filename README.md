![ヘッダー画像](/resourse/readme-header.png)
## GitHubの通知は分散しすぎてわからない！
GitDeckはそんなあなたに向けたサービスです<br>
複数リポジトリの情報を一画面でチェックできたり、issueにも満たないアイデアを投稿することができます

[デモ動画](https://user-images.githubusercontent.com/34413567/124460483-63a7b680-ddca-11eb-88b9-5b6755f1f10a.mov)

## 技育CAMPハッカソン最優秀賞👑
2021年7月3日〜4日に開催された[サポーターズ 技育CAMP ハッカソンvol.5「開発を効率化するアプリケーションを作ろう！」](https://talent.supporterz.jp/events/b89ddfc0-d4d0-4a9a-8092-14376eb89e85/)にて学生4人で制作し、[最優秀賞](https://twitter.com/geek_pjt/status/1411617994032046085?s=20)を受賞しました🎉🎉🎉

ハッカソン成果発表会での発表スライドは[こちら](https://docs.google.com/presentation/d/1OADEi6gixuiuqC9YDkTika9M2B2zQLtKWK73cejNURE/edit?usp=sharing)

## 特徴
### 複数リポジトリの情報を一画面でチェック
![全体スクリーンショット](/resourse/screenshot1.png)
あなたが開発しているリポジトリも気になるOSSも！複数のタイムラインを見やすいインターフェースに統合しています<br>GitHubアカウントと連携しているためプライベートリポジトリも追加可能です。

### 厳選されたタイムライン
![フィルタリング機能](/resourse/filtering.png)

デフォルトではIssueやPullRequestの作成、それらについたコメント、アイデア投稿だけをタイムラインに表示します<br>
加えて**Issue/PullRequestのオープン状態やラベルでフィルタリング**し、タイムラインをカスタマイズすることもできます

### 読みやすい表示
![UI面での工夫](/resourse/ui.png)
- **Markdown対応**
<br>GitHub上と同じ表示で情報をチェックできます
- **カラムの伸縮可能**
<br>一目で様々なリポジトリ情報を確認できる一方で、特定のリポジトリのタイムラインを見たいとき、狭い幅のままではコードや長文が読みにくいでしょう<br>GitDeckではその時々に合わせて読みやすいよう各カラム幅を調整できます
- **同じトピックに関する議論はスレッドに**
<br>同じIssueやPullRequestに関する議論はスレッドにまとめています<br>
コメントが多い時はデフォルトで直近２コメントだけを表示し、「返信をさらに表示」でそれ以外のコメントも表示させます
- **長すぎる投稿は折り畳み式に**
<br>一つの長文でタイムラインが全て埋まるなんてことはありません！
- **GitHubページへのリンク**
<br>GitHub上の元のページを見たくなった時はIssueやPullRequestのタイトルをクリックするだけで該当ページへ遷移します

### ちょっとした提案はアイデアに
![アイデア機能](/resourse/idea.png)
「自信がない」「言うタイミングを見失った」などの理由でチームに共有されずに消えてしまった提案はありませんか？
そのような提案はぜひ"アイデア"として投稿してみましょう<br>
アイデアはGitDeck独自の機能でGitHub上には投稿されないため気軽に投稿することができます<br>
もしかするとあなたのプロダクトを劇的に良くするきっかけになるかもしれません。

### 操作方法がわからなくても大丈夫！
- チュートリアルカラムを用意しているため初見の人でも簡単に操作を覚えることができます
- ローカルストレージにタイムラインの情報を保存しているため誤ってブラウザを閉じてしまっても問題ありません


## 開発体制
<table>
  <tr>
    <th>開発人数</th>
    <td>
      4人<br>
      <b><a href="https://github.com/habara-k"><img src="https://github.com/habara-k.png" width="50px;" /></b>
      <b><a href="https://github.com/knknk98"><img src="https://github.com/knknk98.png" width="50px;" /></b>
      <b><a href="https://github.com/zwwaa-ku"><img src="https://github.com/zwwaa-ku.png" width="50px;" /></b>
      <b><a href="https://github.com/yuta-ike"><img src="https://github.com/yuta-ike.png" width="50px;" /></b>
    </td>
  </tr>
  <tr>
    <th>担当</th>
    <td>
      <a href="https://github.com/habara-k">@keigo habara</a> : バックエンド/フロントエンド(サーバーとの通信周り)<br>
      <a href="https://github.com/knknk98">@knknk98</a> : フロントエンド(UI)<br>
      <a href="https://github.com/zwwaa-ku">@
Nobuaki-M</a> : フロントエンド(UI)<br>
      <a href="https://github.com/knknk98">@yuta-ike</a>：メンター、アイデア出し、一部フロントエンドの実装<br>
    </td>
  </tr>
  <tr>
    <th>開発期間</th>
    <td>約1週間</td>
  </tr>
  <tr>
    <th>主要技術</th>
    <td>フロントエンド：Nuxt.js / TypeScript <br> バックエンド：Flask / GitHubAPI <br> インフラ：Docker</td>
  </tr>
</table>

## ローカルでの実行方法
前提：Dockerがインストールされている / GitHubアカウントを持っている

1. このリポジトリをclone
1. 初回：[こちら](https://github.com/knknk98/issue-twitter/tree/main/backend#readme)を参考にバックエンドの設定を行う<br>
DBのDockerfileがm1 mac仕様になっていますのでご自身の環境によって適宜変えてください
1. ディレクトリ直下で```docker-compose up```
1. localhost:3000にアクセス

## Special Thanks🎉
開発に協力してくれた情ピカさん、岡部さん、KoukiNAGATAさん

開発のきっかけであるハッカソンを開催していただいたサポーターズさん
