# -*- coding: utf-8 -*-
import fire
import testcase_datastore
import testcase_presenter


def create_test_result_report(input_path: str, output_path: str, commit_id: str) -> None:
    """Markdown形式で記述したテストケースをExcel形式のテスト結果報告書に変換するツール

    Arguments:
    input_path: テストケースを記述したMarkdownのパス
    output_path: 生成したExcelを出力するパス
    commit_id: テストケース及び対向する設計書はgitで管理する前提であり，どのコミットIDで生成されたかを指定する.

    Returns:
    None

    実行すると入力したテストケースに基づき，指定したディレクトリにテスト結果報告書(エクセル形式)が出力される。

    変換するMarkdownは以下の形式で記述する::

        - テスト対象: [テスト対象を記載する] e.g. 画面
            - テスト目的: [テスト目的を記載する] e.g. スクロールする
                - テスト条件: [テスト条件を記載する] e.g. 50>入力値の場合
                    - 前提条件
                        - [前提条件を記載する．複数行記載可能．0行以上] e.g. データNo.5をインポートすること
                    - 手順
                        1. [手順を記載する．複数行記載可能．0行以上] e.g. No.6をタップする
                    - 期待値
                        - [期待値を記載する．複数行記載可能．0行以上] e.g. No10.選択状態=選択となること
                    - 導出方法
                        - [導出方法を記載する．複数行記載可能．0行以上] e.g. No10の初期値を境界値分析
                    - 備考
                        - [備考を記載する．複数行記載可能．0行以上]
                - テスト条件: 同じ「テスト対象」「テスト目的」の場合，それらの記載は省略できる．
                    ...
            - テスト目的: 同じ「テスト対象」の場合，その記載は省略できる．
                ...
    """

    # テストケースを指定したファイルから取得する
    test_cases = testcase_datastore.TestCaseDataStore.read(input_path)

    # 取得したテストケースをテスト結果報告書として出力
    testcase_presenter.TestCasePresenter.output_test_result_report(test_cases, output_path)


if __name__ == '__main__':
    fire.Fire(create_test_result_report)
