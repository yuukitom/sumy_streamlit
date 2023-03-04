import spacy
import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.kl import KLSummarizer

# 変数定義
nlp = spacy.load("ja_ginza_electra")
parser = None
input_data = None

# 要約の準備をする関数
def exe_summary(input_data):
  document = "".join(input_data).replace("　", "").replace(" ", "").replace("\n", "").replace("\r", "")
  
  corpus = []
  originals = []
  doc = nlp(document)
  
   # spaCyは、「sents」で文章全体のセンテンスを取得できる
  for s in doc.sents:
    originals.append(s)
    tokens = []
    # レンマ化したトークンを追加
    for t in s:
      tokens.append(t.lemma_)
    corpus.append(" ".join(tokens))
    
  parser = PlaintextParser.from_string("".join(corpus), Tokenizer("japanese"))
  
  return parser, originals, corpus


# 要約用のアルゴリズムを実行する
def summarize(summarizer, parser, originals, corpus):
  summarizer.stop_words = [' ']  # スペースも1単語として認識されるため、ストップワードにすることで除外する
  result = summarizer(document=parser.document, sentences_count=sentences)
  st.write(corpus)
  for sentence in result:
    st.write(originals[corpus.index(sentence.__str__())])
   
# インターフェイスの表示
st.title('文章要約アプリ')

# ファイル選択
st.write("### 要約ファイル選択")
uploaded_file = st.file_uploader("テキストファイルをアップロードしてください。", ["txt"])

if uploaded_file is not None:
  content = uploaded_file.read()
  input_data = content.decode()
  
if input_data is not None:
  st.write(input_data)
  
# 要約結果の行数を表示
st.write("### 要約結果行数選択")
sentences = st.slider("何行に要約しますか", 3, 10, 3)

# 要約実行関数を呼び出し
st.write("### 要約実行")
algori = st.selectbox(
	"要約アルゴリズムを選択してください",
 ("LexRank", "Lsa", "Reduction", "Luhn", "SumBasic")
)
st.write("要約を開始しますか？")
if st.button("開始"):
  parser, originals, corpus = exe_summary(input_data)

  
# 要約を実行し結果の表示
if parser is not None:
  st.write("### 結果の表示")
  # st.write(originals)
  if algori == "LexRank":
    summarize(LexRankSummarizer(), parser, originals, corpus)
  elif algori == "Lsa":
    summarize(LsaSummarizer(), parser, originals, corpus)
  elif algori == "Reduction":
    summarize(ReductionSummarizer(), parser, originals, corpus)
  elif algori == "Luhn":
    summarize(LuhnSummarizer(), parser, originals, corpus)
  else:
    summarize(SumBasicSummarizer(), parser, originals, corpus)
    
