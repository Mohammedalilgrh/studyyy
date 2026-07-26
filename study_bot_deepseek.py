import asyncio
import logging
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import tempfile
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)
from telegram.constants import ParseMode

# AI Libraries
import pytesseract
from PIL import Image
import PyPDF2
import docx

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Configuration
BOT_TOKEN = "7954243581:AAFB_eQHGwCLRYTGeBwJ3gZWa1qtMDT76Bs"
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key-here"  # Get from https://platform.deepseek.com/
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

class StudyBot:
    def __init__(self):
        self.user_sessions = {}
        self.api_key = DEEPSEEK_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='ara+eng')
            return text
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            return ""
    
    def call_deepseek_api(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Make API call to DeepSeek"""
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            response = requests.post(
                DEEPSEEK_API_URL,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {e}")
            return None
    
    async def generate_questions(self, content: str, language: str = "mixed") -> List[Dict]:
        """Generate exam questions using DeepSeek"""
        try:
            system_prompt = """You are an expert exam creator for bilingual (Arabic/English) education. 
            You MUST respond with valid JSON only, no additional text.
            Generate diverse questions that test understanding, not just memorization."""
            
            user_prompt = f"""
            Based on the following content, generate 5 diverse exam questions.
            Content: {content[:4000]}
            
            Language: {language}
            - If content has Arabic, include some Arabic questions
            - If content is English, use English
            - Mix languages if the content is mixed
            
            IMPORTANT: Respond ONLY with a valid JSON object in this exact format:
            {{
                "questions": [
                    {{
                        "id": 1,
                        "type": "multiple_choice",
                        "question": "Question text here",
                        "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                        "correct_answer": "A",
                        "explanation": "Why this answer is correct"
                    }},
                    {{
                        "id": 2,
                        "type": "true_false",
                        "question": "Statement here",
                        "correct_answer": "True",
                        "explanation": "Explanation here"
                    }},
                    {{
                        "id": 3,
                        "type": "short_answer",
                        "question": "Question requiring brief answer",
                        "model_answer": "Expected answer",
                        "keywords": ["keyword1", "keyword2"]
                    }},
                    {{
                        "id": 4,
                        "type": "multiple_choice",
                        "question": "Another multiple choice question",
                        "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                        "correct_answer": "C",
                        "explanation": "Explanation here"
                    }},
                    {{
                        "id": 5,
                        "type": "short_answer",
                        "question": "Final question",
                        "model_answer": "Expected answer",
                        "keywords": ["keyword1", "keyword2"]
                    }}
                ]
            }}
            
            Make questions progressively harder and cover different aspects of the content.
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response_text = self.call_deepseek_api(messages, temperature=0.7, max_tokens=2000)
            
            if response_text:
                # Clean the response to extract JSON
                response_text = response_text.strip()
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]
                
                questions_data = json.loads(response_text)
                return questions_data.get("questions", [])
            else:
                logger.error("Failed to get response from DeepSeek")
                return []
                
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from DeepSeek: {e}")
            return []
        except Exception as e:
            logger.error(f"Error generating questions: {e}")
            return []
    
    async def grade_answer(self, question: Dict, user_answer: str) -> Dict:
        """Grade a single answer"""
        try:
            if question["type"] == "multiple_choice":
                user_letter = user_answer.strip().upper()
                if user_letter and user_letter[0] == question["correct_answer"]:
                    is_correct = True
                    score = 100
                else:
                    is_correct = False
                    score = 0
                
                return {
                    "score": score,
                    "is_correct": is_correct,
                    "feedback": "✅ Correct!" if is_correct else "❌ Incorrect",
                    "correct_answer": question["correct_answer"],
                    "explanation": question.get("explanation", "")
                }
                
            elif question["type"] == "true_false":
                user_answer_clean = user_answer.strip().lower()
                correct_answer_clean = question["correct_answer"].strip().lower()
                
                is_correct = user_answer_clean == correct_answer_clean
                score = 100 if is_correct else 0
                
                return {
                    "score": score,
                    "is_correct": is_correct,
                    "feedback": "✅ Correct!" if is_correct else "❌ Incorrect",
                    "correct_answer": question["correct_answer"],
                    "explanation": question.get("explanation", "")
                }
                
            elif question["type"] == "short_answer":
                system_prompt = """You are an expert grader. Evaluate the student's answer against the model answer.
                Be fair but strict. Consider partial credit for partially correct answers.
                Return ONLY a JSON object, no other text."""
                
                user_prompt = f"""
                Question: {question['question']}
                Model Answer: {question['model_answer']}
                Keywords: {', '.join(question.get('keywords', []))}
                Student's Answer: {user_answer}
                
                Grade this answer from 0-100 based on accuracy and completeness.
                Return ONLY this JSON format:
                {{
                    "score": 85,
                    "feedback": "Your answer is mostly correct but missing...",
                    "missing_points": "What you missed...",
                    "suggestion": "How to improve..."
                }}
                """
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                
                response_text = self.call_deepseek_api(messages, temperature=0.3, max_tokens=300)
                
                if response_text:
                    response_text = response_text.strip()
                    if "```json" in response_text:
                        response_text = response_text.split("```json")[1].split("```")[0]
                    elif "```" in response_text:
                        response_text = response_text.split("```")[1].split("```")[0]
                    
                    result = json.loads(response_text)
                    result["correct_answer"] = question.get("model_answer", "")
                    result["explanation"] = result.get("suggestion", "")
                    return result
                else:
                    return {
                        "score": 0,
                        "feedback": "Could not evaluate answer",
                        "correct_answer": question.get("model_answer", ""),
                        "explanation": ""
                    }
            
            return {
                "score": 0,
                "feedback": "Error grading answer",
                "correct_answer": "",
                "explanation": ""
            }
            
        except Exception as e:
            logger.error(f"Error grading answer: {e}")
            return {
                "score": 0,
                "feedback": f"Error grading: {str(e)}",
                "correct_answer": "",
                "explanation": ""
            }
    
    def calculate_final_grade(self, grades: List[Dict]) -> Dict:
        """Calculate overall exam grade"""
        if not grades:
            return {
                "total_score": 0,
                "percentage": 0,
                "letter_grade": "N/A",
                "emoji": "❓",
                "grades": []
            }
        
        total_possible = len(grades) * 100
        total_earned = sum(g["score"] for g in grades)
        percentage = (total_earned / total_possible) * 100 if total_possible > 0 else 0
        
        if percentage >= 90:
            letter_grade = "A"
            emoji = "🏆"
        elif percentage >= 80:
            letter_grade = "B"
            emoji = "🌟"
        elif percentage >= 70:
            letter_grade = "C"
            emoji = "👍"
        elif percentage >= 60:
            letter_grade = "D"
            emoji = "📚"
        else:
            letter_grade = "F"
            emoji = "💪"
        
        return {
            "total_score": f"{total_earned}/{total_possible}",
            "percentage": round(percentage, 2),
            "letter_grade": letter_grade,
            "emoji": emoji,
            "grades": grades
        }

# Initialize bot instance
study_bot = StudyBot()

# Bot command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user = update.effective_user
    
    welcome_message = f"""
*🎓 مرحباً {user.first_name}! | Welcome {user.first_name}! 🎓*

*Smart Study Bot | بوت الدراسة الذكي*
_Your AI-powered study assistant | مساعدك الدراسي الذكي_

📚 *What I can do | ماذا يمكنني أن أفعل:*
• 📖 Analyze books, documents & images
• 📝 Generate exam-style questions
• ✅ Grade your answers instantly
• 📊 Provide detailed feedback & corrections

📁 *Supported formats | التنسيقات المدعومة:*
• PDF, DOCX, TXT files
• Images (JPG, PNG) with OCR
• Arabic & English content

🚀 *Quick Start | بداية سريعة:*
1️⃣ Send /exam to start
2️⃣ Upload your study material
3️⃣ Answer the questions
4️⃣ Get your results!

*Powered by DeepSeek AI | مدعوم بـ DeepSeek AI*
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📝 Start Exam | بدء اختبار", callback_data="start_exam"),
            InlineKeyboardButton("ℹ️ Help | مساعدة", callback_data="show_help")
        ],
        [
            InlineKeyboardButton("📊 My Stats | إحصائياتي", callback_data="show_stats"),
            InlineKeyboardButton("❌ Cancel | إلغاء", callback_data="cancel_exam")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def exam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start exam session"""
    user_id = update.effective_user.id
    study_bot.user_sessions[user_id] = {
        "state": "waiting_for_content",
        "questions": [],
        "current_question": 0,
        "answers": [],
        "grades": [],
        "start_time": datetime.now()
    }
    
    message = """
📚 *Exam Session Started | بدأت جلسة الاختبار*

Please send me your study material:
• 📄 Documents (PDF, DOCX, TXT)
• 🖼️ Images with text (JPG, PNG)
• 💬 Direct text message

أرسل لي المادة الدراسية:
• 📄 مستندات (PDF, DOCX, TXT)
• 🖼️ صور تحتوي على نص (JPG, PNG)
• 💬 رسالة نصية مباشرة
"""
    
    keyboard = [[InlineKeyboardButton("❌ Cancel | إلغاء", callback_data="cancel_exam")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle received documents"""
    user_id = update.effective_user.id
    document = update.message.document
    
    if document.file_size > 20 * 1024 * 1024:
        await update.message.reply_text(
            "❌ File too large! Please send files under 20MB.\n"
            "❌ الملف كبير جداً! يرجى إرسال ملفات أقل من 20 ميجابايت."
        )
        return
    
    processing_msg = await update.message.reply_text(
        "📄 *Processing document...*\n⏳ _Extracting text..._\n🤖 _Analyzing content..._",
        parse_mode=ParseMode.MARKDOWN
    )
    
    file = await context.bot.get_file(document.file_id)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(document.file_name)[1]) as tmp_file:
        await file.download_to_drive(tmp_file.name)
        file_path = tmp_file.name
    
    text = ""
    file_ext = document.file_name.lower()
    
    if file_ext.endswith('.pdf'):
        text = study_bot.extract_text_from_pdf(file_path)
    elif file_ext.endswith('.docx'):
        text = study_bot.extract_text_from_docx(file_path)
    elif file_ext.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif file_ext.endswith(('.jpg', '.jpeg', '.png')):
        text = study_bot.extract_text_from_image(file_path)
    
    try:
        os.unlink(file_path)
    except:
        pass
    
    if text.strip():
        await processing_msg.edit_text(
            "✅ *Text extracted successfully!*\n🤖 *Generating questions...*",
            parse_mode=ParseMode.MARKDOWN
        )
        await process_content(update, context, text, processing_msg)
    else:
        await processing_msg.edit_text(
            "❌ *Could not extract text from the file*\nPlease try a different format or send text directly.",
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id in study_bot.user_sessions:
        session = study_bot.user_sessions[user_id]
        
        if session["state"] == "waiting_for_content":
            if len(text) < 50:
                await update.message.reply_text(
                    "⚠️ *Text too short!* Please send more content (at least 50 characters).",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            processing_msg = await update.message.reply_text(
                "🤖 *Analyzing content and generating questions...*",
                parse_mode=ParseMode.MARKDOWN
            )
            await process_content(update, context, text, processing_msg)
            
        elif session["state"] == "answering":
            await process_answer(update, context, text)
    else:
        keyboard = [[InlineKeyboardButton("📝 Start Exam | بدء اختبار", callback_data="start_exam")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "👋 *Start an exam session first!*\nUse /exam command or tap below:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages"""
    processing_msg = await update.message.reply_text(
        "📸 *Processing image...*\n⏳ _Running OCR to extract text..._",
        parse_mode=ParseMode.MARKDOWN
    )
    
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        await file.download_to_drive(tmp_file.name)
        file_path = tmp_file.name
    
    text = study_bot.extract_text_from_image(file_path)
    
    try:
        os.unlink(file_path)
    except:
        pass
    
    if text.strip():
        await processing_msg.edit_text(
            "✅ *Text extracted from image!*\n🤖 *Generating questions...*",
            parse_mode=ParseMode.MARKDOWN
        )
        await process_content(update, context, text, processing_msg)
    else:
        await processing_msg.edit_text(
            "❌ *No text detected in image*\nPlease try a clearer image or send text directly.",
            parse_mode=ParseMode.MARKDOWN
        )

async def process_content(update: Update, context: ContextTypes.DEFAULT_TYPE, content: str, status_msg=None):
    """Process content and generate questions"""
    user_id = update.effective_user.id
    session = study_bot.user_sessions.get(user_id, {})
    
    has_arabic = any('\u0600' <= char <= '\u06ff' for char in content)
    language = "mixed" if has_arabic else "english"
    
    session["content"] = content[:1000]
    session["language"] = language
    
    questions = await study_bot.generate_questions(content, language)
    
    if questions and len(questions) > 0:
        session["questions"] = questions
        session["state"] = "answering"
        session["current_question"] = 0
        session["answers"] = []
        session["grades"] = []
        study_bot.user_sessions[user_id] = session
        
        if status_msg:
            await status_msg.delete()
        
        await update.message.reply_text(
            f"📝 *Exam Ready!*\n📊 Questions: {len(questions)}\n🌍 Language: {language.upper()}\n\n_Good luck! 🍀_",
            parse_mode=ParseMode.MARKDOWN
        )
        
        await send_question(update, context, questions[0], 0, len(questions))
    else:
        if status_msg:
            await status_msg.delete()
        
        await update.message.reply_text(
            "❌ *Failed to generate questions*\nPlease try with different content or format.",
            parse_mode=ParseMode.MARKDOWN
        )

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question: Dict, q_num: int, total: int):
    """Send a question to the user"""
    type_emoji = {
        "multiple_choice": "🔤",
        "true_false": "✅",
        "short_answer": "✍️"
    }
    
    emoji = type_emoji.get(question["type"], "❓")
    
    message = f"{emoji} *Question {q_num + 1}/{total}*\n\n"
    message += f"*{question['question']}*\n\n"
    
    if question["type"] == "multiple_choice":
        for option in question["options"]:
            message += f"`{option}`\n"
        message += "\n_Reply with the letter (A, B, C, or D)_"
        
    elif question["type"] == "true_false":
        message += "`True` or `False`?\n_Reply with True or False_"
        
    elif question["type"] == "short_answer":
        message += "_Write your answer in detail_ | _اكتب إجابتك بالتفصيل_"
    
    keyboard = []
    if q_num > 0:
        keyboard.append(InlineKeyboardButton("⏭️ Skip | تخطي", callback_data="skip_question"))
    keyboard.append(InlineKeyboardButton("❌ End Exam | إنهاء", callback_data="end_exam"))
    
    reply_markup = InlineKeyboardMarkup([keyboard]) if keyboard else None
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def process_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, answer: str):
    """Process user's answer"""
    user_id = update.effective_user.id
    session = study_bot.user_sessions[user_id]
    current_q = session["current_question"]
    
    if current_q >= len(session["questions"]):
        await update.message.reply_text("Exam is already complete! Use /exam to start a new one.")
        return
    
    question = session["questions"][current_q]
    
    grading_msg = await update.message.reply_text(
        "🤖 *Grading your answer...* | *جاري تصحيح إجابتك...*",
        parse_mode=ParseMode.MARKDOWN
    )
    
    grade = await study_bot.grade_answer(question, answer)
    session["grades"].append(grade)
    session["answers"].append({
        "question": question["question"],
        "user_answer": answer,
        "correct_answer": grade.get("correct_answer", ""),
        "score": grade["score"]
    })
    
    await grading_msg.delete()
    
    feedback_message = ""
    
    if grade["score"] == 100:
        feedback_message += "✅ *Excellent!*\n\n"
    elif grade["score"] >= 70:
        feedback_message += "👍 *Good!*\n\n"
    elif grade["score"] >= 50:
        feedback_message += "📚 *Keep trying!*\n\n"
    else:
        feedback_message += "💪 *Don't give up!*\n\n"
    
    feedback_message += f"*Your Answer:* _{answer}_\n"
    feedback_message += f"*Score:* `{grade['score']}/100`\n\n"
    
    if "feedback" in grade and grade["feedback"]:
        feedback_message += f"*Feedback:* {grade['feedback']}\n\n"
    
    if "correct_answer" in grade and grade["correct_answer"]:
        feedback_message += f"*Correct Answer:* `{grade['correct_answer']}`\n"
    
    if "explanation" in grade and grade["explanation"]:
        feedback_message += f"*Explanation:* _{grade['explanation']}_\n"
    
    await update.message.reply_text(feedback_message, parse_mode=ParseMode.MARKDOWN)
    
    session["current_question"] += 1
    study_bot.user_sessions[user_id] = session
    
    if session["current_question"] < len(session["questions"]):
        await asyncio.sleep(1)
        next_q = session["questions"][session["current_question"]]
        await send_question(update, context, next_q, session["current_question"], len(session["questions"]))
    else:
        await finish_exam(update, context)

async def finish_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finish exam and show results"""
    user_id = update.effective_user.id
    session = study_bot.user_sessions.get(user_id, {})
    
    if not session.get("grades"):
        await update.message.reply_text("No answers were recorded. Start a new exam with /exam")
        return
    
    result = study_bot.calculate_final_grade(session["grades"])
    
    time_taken = "N/A"
    if "start_time" in session:
        elapsed = datetime.now() - session["start_time"]
        minutes = elapsed.seconds // 60
        seconds = elapsed.seconds % 60
        time_taken = f"{minutes}m {seconds}s"
    
    message = f"""
{result['emoji']} *EXAM RESULTS | نتائج الاختبار* {result['emoji']}

📊 *Overall Performance:*
• Total Score: `{result['total_score']}`
• Percentage: `{result['percentage']}%`
• Grade: `{result['letter_grade']}`
• Time: `{time_taken}`

📝 *Question Breakdown:*
"""
    
    for i, (question, answer_data, grade) in enumerate(zip(
        session["questions"], session["answers"], session["grades"]
    ), 1):
        q_text = question['question'][:80] + "..." if len(question['question']) > 80 else question['question']
        
        if grade["score"] == 100:
            score_emoji = "✅"
        elif grade["score"] >= 50:
            score_emoji = "⚠️"
        else:
            score_emoji = "❌"
        
        message += f"\n{score_emoji} *Q{i}:* {q_text}\n"
        message += f"   Your Answer: `{answer_data['user_answer'][:50]}`\n"
        message += f"   Score: `{grade['score']}/100`\n"
    
    if result['percentage'] >= 90:
        message += "\n🏆 *Outstanding!* You've mastered this material!"
    elif result['percentage'] >= 80:
        message += "\n🌟 *Great job!* You have a strong understanding!"
    elif result['percentage'] >= 70:
        message += "\n👍 *Good work!* Keep practicing to improve!"
    elif result['percentage'] >= 60:
        message += "\n📚 *Fair effort!* Review the material and try again!"
    else:
        message += "\n💪 *Keep studying!* Review the corrections and try again!"
    
    keyboard = [
        [
            InlineKeyboardButton("📝 New Exam | اختبار جديد", callback_data="start_exam"),
            InlineKeyboardButton("🔄 Retry | إعادة", callback_data="retry_exam")
        ],
        [
            InlineKeyboardButton("📊 Review | مراجعة", callback_data="detailed_review"),
            InlineKeyboardButton("📤 Share | مشاركة", callback_data="share_results")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    session["state"] = "completed"
    session["results"] = result
    study_bot.user_sessions[user_id] = session

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if query.data == "start_exam":
        study_bot.user_sessions[user_id] = {
            "state": "waiting_for_content",
            "questions": [],
            "current_question": 0,
            "answers": [],
            "grades": [],
            "start_time": datetime.now()
        }
        await query.edit_message_text(
            "📚 *New Exam Session*\n\nSend me your study material to begin!\nأرسل لي المادة الدراسية للبدء!",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif query.data == "show_help":
        help_text = """
🤖 *STUDY BOT HELP | مساعدة البوت*

*Getting Started:*
1️⃣ `/exam` - Start new exam
2️⃣ Send your study material
3️⃣ Answer the questions
4️⃣ Get instant feedback

*Supported Content:*
📄 Documents: PDF, DOCX, TXT
🖼️ Images: JPG, PNG (with text)
💬 Direct text messages

*Question Types:*
🔤 Multiple Choice
✅ True/False
✍️ Short Answer

*Commands:*
/start - Main menu
/exam - New exam
/help - This help
/cancel - Cancel exam

*Tips:*
• Send clear, readable content
• Detailed answers get better feedback
• You can skip questions
• Review your mistakes to learn

*Powered by DeepSeek AI*
        """
        await query.edit_message_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    elif query.data == "show_stats":
        await query.edit_message_text(
            "📊 *Statistics feature coming soon!*\nComplete more exams to track your progress.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif query.data == "cancel_exam":
        if user_id in study_bot.user_sessions:
            del study_bot.user_sessions[user_id]
        await query.edit_message_text(
            "✅ *Exam cancelled*\nUse /exam to start a new one.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif query.data == "skip_question":
        session = study_bot.user_sessions.get(user_id)
        if session and session["state"] == "answering":
            session["grades"].append({
                "score": 0,
                "feedback": "Question skipped",
                "correct_answer": "",
                "explanation": ""
            })
            session["answers"].append({
                "question": session["questions"][session["current_question"]]["question"],
                "user_answer": "SKIPPED",
                "correct_answer": "",
                "score": 0
            })
            
            session["current_question"] += 1
            
            if session["current_question"] < len(session["questions"]):
                next_q = session["questions"][session["current_question"]]
                await query.edit_message_text("⏭️ Question skipped! Moving to next...")
                await asyncio.sleep(1)
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"🔤 *Question {session['current_question'] + 1}/{len(session['questions'])}*\n\n*{next_q['question']}*",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await query.edit_message_text("📝 Exam complete! Calculating results...")
                await asyncio.sleep(1)
                # Simplified finish for callback
                result = study_bot.calculate_final_grade(session["grades"])
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"📊 *Results:* {result['total_score']} - {result['percentage']}% - Grade: {result['letter_grade']}",
                    parse_mode=ParseMode.MARKDOWN
                )
            
            study_bot.user_sessions[user_id] = session
    
    elif query.data == "end_exam":
        session = study_bot.user_sessions.get(user_id)
        if session and session["state"] == "answering":
            await query.edit_message_text("📝 Ending exam... Calculating results...")
            await asyncio.sleep(1)
            result = study_bot.calculate_final_grade(session["grades"])
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"📊 *Results:* {result['total_score']} - {result['percentage']}% - Grade: {result['letter_grade']}",
                parse_mode=ParseMode.MARKDOWN
            )
    
    elif query.data == "retry_exam":
        session = study_bot.user_sessions.get(user_id)
        if session and "content" in session:
            session["state"] = "answering"
            session["current_question"] = 0
            session["answers"] = []
            session["grades"] = []
            session["start_time"] = datetime.now()
            study_bot.user_sessions[user_id] = session
            
            if session["questions"]:
                first_q = session["questions"][0]
                await query.edit_message_text("🔄 *Retrying exam... Good luck!*", parse_mode=ParseMode.MARKDOWN)
                await asyncio.sleep(1)
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"🔤 *Question 1/{len(session['questions'])}*\n\n*{first_q['question']}*",
                    parse_mode=ParseMode.MARKDOWN
                )
    
    elif query.data == "detailed_review":
        session = study_bot.user_sessions.get(user_id)
        if session and session.get("grades"):
            review_message = "*📊 DETAILED REVIEW | مراجعة مفصلة*\n\n"
            
            for i, (question, answer_data, grade) in enumerate(zip(
                session["questions"], session["answers"], session["grades"]
            ), 1):
                review_message += f"*Q{i}:* {question['question'][:100]}...\n"
                review_message += f"Your Answer: `{answer_data['user_answer'][:50]}`\n"
                review_message += f"Score: `{grade['score']}/100`\n"
                if grade.get("explanation"):
                    review_message += f"Note: _{grade['explanation'][:100]}_\n"
                review_message += "\n"
            
            await query.edit_message_text(review_message, parse_mode=ParseMode.MARKDOWN)
    
    elif query.data == "share_results":
        await query.edit_message_text(
            "📤 *Share feature coming soon!*\nYou'll be able to share your results with friends.",
            parse_mode=ParseMode.MARKDOWN
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler"""
    help_text = """
🤖 *STUDY BOT HELP | مساعدة البوت*

*Quick Start:*
1️⃣ Send /exam
2️⃣ Upload study material
3️⃣ Answer questions
4️⃣ Get results!

*Supported:*
📄 PDF, DOCX, TXT
🖼️ Images (OCR)
💬 Text messages
🌍 Arabic & English

*Questions Types:*
• Multiple Choice
• True/False
• Short Answer

*Powered by DeepSeek AI*
"""
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel current operation"""
    user_id = update.effective_user.id
    if user_id in study_bot.user_sessions:
        del study_bot.user_sessions[user_id]
    
    keyboard = [[InlineKeyboardButton("📝 New Exam | اختبار جديد", callback_data="start_exam")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ *Operation cancelled*\nStart a new exam anytime with /exam",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

def main():
    """Main function to run the bot"""
    if DEEPSEEK_API_KEY == "sk-your-deepseek-api-key-here":
        print("⚠️ WARNING: Please set your DeepSeek API key in the code!")
        print("Get your API key from: https://platform.deepseek.com/")
        print("The bot will start but question generation will fail without a valid API key.\n")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("exam", exam_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Study Bot is starting...")
    print("✅ Bot is now running! Press Ctrl+C to stop.")
    print("📱 Open Telegram and send /start to your bot!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
