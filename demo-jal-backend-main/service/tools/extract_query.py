from service.clients.llm_router import LLMRouter
from service.schemas.schemas import ClientQuestions


class ExtractQuery:
    def __init__(self):
        # self.client = OllamaServer()
        self.llm_router = LLMRouter()
        self.system_prompt = """
        【役割】多人対話内容分析の専門家

        【タスク】多人対話の文字起こしテキストから重要な情報を抽出する

        【入力】多人対話の完全な文字起こしテキスト

        【核心原則】
        ✅ 重要情報の識別：対話中の重要な事実、決定、情報ポイントを抽出
        ✅ 構造化整理：情報を明確で整理された要点にまとめる
        ✅ 原意に忠実：元の対話の情報意図を正確に保持する
        
        【出力規範】
        1. 抽出された情報はMarkdown形式の項目として列挙
        2. 各情報は簡潔かつ完全な内容で
        3. 口癖、重複内容、無関係な社交辞令を除去
        4. 対話での情報の出現順に配列
        
        【例】
        対話の一部：
        "佐藤：皆さん、こんにちは。新製品の発表について、来週の火曜日に行うことにしました。
        鈴木：予算はどのくらいですか？宣伝資料を準備する必要がありますか？
        田中：予算は3万円以内に抑え、宣伝資料はマーケティング部が担当します。"
        
        抽出結果：
        - 新製品の発表は来週火曜日に決定
        - プロジェクト予算は3万円以内に抑制
        - 宣伝資料はマーケティング部が担当
        
        【注意事項】
        - 対話中の重要な事実、決定、重要情報を識別・抽出
        - 多人対話には複数の情報ポイントが含まれる可能性があり、すべて抽出する必要あり
        - 挨拶などの非重要内容は無視
        - 曖昧な内容には最も合理的な解釈を採用
        - 抽出された情報は必ず日本語で記述すること

        【出力形式】
        Markdown形式で出力し、各情報はダッシュで始める：
        - 重要情報1
        - 重要情報2
        - ...
        """

        self.user_prompt = """
        以下は多人対話の完全な文字起こし内容です。すべての重要情報を抽出し、日本語でMarkdown形式の項目として列挙してください：
        
        {conversation_transcript}
        """

    def extract_informations(self, conversation_transcript, provider):
        """
        Extract customer questions from a conversation transcript

        Args:
            conversation_transcript (str): The full conversation transcript

        Returns:
            list: A list of extracted customer questions
        """
        response = self.llm_router.generate(
            self.system_prompt,
            self.user_prompt.format(conversation_transcript=conversation_transcript),
            response_format=ClientQuestions,
            temperature=0,
            provider=provider,
        )

        return response
