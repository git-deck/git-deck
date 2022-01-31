![ヘッダー画像](/resourse/readme-header.png)
## GitHubの通知は分散しすぎてわからない！
GitDeckはそんなあなたに向けたサービスです<br>
複数リポジトリの情報を一画面でチェックできます

[デモ動画](https://user-images.githubusercontent.com/34413567/134767993-63f1ecb0-d04f-4234-973f-c3415f34ff38.mov)

## 技育祭-開発／スキル支援部門最優秀賞👑
2021年9月18日~26日に開催された[技育祭2021](https://talent.supporterz.jp/geekten/2021/)にて学生4人で参加し、[最優秀賞](https://twitter.com/chomado/status/1446741326834196481?s=21)を受賞しました🎉🎉🎉

成果発表会での発表スライドは[こちら](https://docs.google.com/presentation/d/1gaIuLKgB1BZHXGivJvaIdvWa7A8XjAG1gczU-KWtSA0/edit#slide=id.gf2a8ff186d_0_68)

## 技育CAMPハッカソン最優秀賞👑
2021年7月3日〜4日に開催された[サポーターズ 技育CAMP ハッカソンvol.5「開発を効率化するアプリケーションを作ろう！」](https://talent.supporterz.jp/events/b89ddfc0-d4d0-4a9a-8092-14376eb89e85/)にて学生4人で制作し、[最優秀賞](https://twitter.com/geek_pjt/status/1411617994032046085?s=20)を受賞しました🎉🎉🎉

ハッカソン成果発表会での発表スライドは[こちら](https://docs.google.com/presentation/d/1OADEi6gixuiuqC9YDkTika9M2B2zQLtKWK73cejNURE/edit?usp=sharing)

## 特徴
### 複数リポジトリの情報を一画面でチェック
![全体スクリーンショット](/resourse/screenshot1.png)
あなたが開発しているリポジトリも気になるOSSも！複数のタイムラインを見やすいインターフェースに統合しています<br>GitHubアカウントと連携しているためプライベートリポジトリも追加可能です。

### 厳選されたタイムライン
![フィルタリング機能](/resourse/画像1.png)

デフォルトではIssueやPullRequestの作成、それらについたコメントをタイムラインに表示します<br>
加えて**Issue/PullRequestのオープン状態やラベルでフィルタリング**し、タイムラインをカスタマイズすることもできます

### 読みやすい表示
![UI面での工夫](/resourse/ui.png)
- **Markdown対応**
<br>GitHub上と同じ表示で情報をチェックできます
- **シンタックスハイライト**
<br>コード内を色付けして見やすくします
- **カラムの伸縮可能**
<br>一目で様々なリポジトリ情報を確認できる一方で、特定のリポジトリのタイムラインを見たいとき、狭い幅のままではコードや長文が読みにくいでしょう<br>GitDeckではその時々に合わせて読みやすいよう各カラム幅を調整できます
- **同じトピックに関する議論はスレッドに**
<br>同じIssueやPullRequestに関する議論はスレッドにまとめています<br>
コメントが多い時はデフォルトで直近２コメントだけを表示し、「返信をさらに表示」でそれ以外のコメントも表示させます
- **長すぎる投稿は折り畳み式に**
<br>一つの長文でタイムラインが全て埋まるなんてことはありません！
- **GitHubページへのリンク**
<br>GitHub上の元のページを見たくなった時はIssueやPullRequestのタイトルをクリックするだけで該当ページへ遷移します
- **darkmode対応**
<br>開発者御用達！ダークモードに変更できます

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
      <a href="https://github.com/zwwaa-ku">@Nobuaki-M</a> : フロントエンド(UI)<br>
      <a href="https://github.com/yuta-ike">@yuta-ike</a>：メンター、アイデア出し、一部フロントエンドの実装<br>
    </td>
  </tr>
  <tr>
    <th>開発期間</th>
    <td>約1か月</td>
  </tr>
  <tr>
    <th>主要技術</th>
    <td>フロントエンド：Nuxt.js / TypeScript <br> バックエンド：GitHubAPI <br> インフラ：Docker</td>
  </tr>
</table>



## Special Thanks🎉
開発に協力してくれた情ピカさん、岡部さん、KoukiNAGATAさん

開発のきっかけであるハッカソンを開催していただいたサポーターズさん
