DROP TABLE IF EXISTS `movie`;

pragma encoding=utf8;
CREATE TABLE `movie` (
       `id`          INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
       `keyword`     text        NOT NULL DEFAULT '',       -- 検索キーワード
       `title`       text        NOT NULL DEFAULT '',       -- 動画タイトル
       `status`      varchar(10) NOT NULL DEFAULT '',       -- 閲覧権限ステータス
       `view_num`    INTEGER     NOT NULL DEFAULT 0,        --  閲覧数
       `album_num`   INTEGER     NOT NULL DEFAULT 0,        -- アルバム数
       `comment_num` INTEGER     NOT NULL DEFAULT 0,        -- コメント数
       `comment`     text        NOT NULL DEFAULT '',       -- 動画コメント
       `user_name`   text        NOT NULL DEFAULT '',       -- ユーザー名
       `image_link`  varchar(80) NOT NULL DEFAULT '',       -- 画像リンク
       `link`        varchar(80) NOT NULL DEFAULT '',       -- 動画リンク
       `favorite`    TINYINT     NOT NULL DEFAULT 0,        -- お気に入りかどうか
       `active`      TINYINT     NOT NULL DEFAULT 0,        -- お蔵いりかどうか
       `update_at`   datestamp   DEFAULT CURRENT_TIMESTAMP, -- 最終取得日
       UNIQUE(`title`)
);
