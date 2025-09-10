# Quiz Generator using Langchain and Gemini

A powerful and interactive quiz generation application built with Streamlit, Langchain, and Google's Gemini AI. Generate customized multiple-choice quizzes on any topic with intelligent question parsing and real-time feedback.

## 🚀 Features

- **AI-Powered Question Generation**: Leverages Google's Gemini 1.5 Flash model for intelligent quiz creation
- **Customizable Parameters**: Choose difficulty level, number of questions, and topic context
- **Real-time Feedback**: Instant validation with color-coded responses
- **Progressive Difficulty**: Smart question generation that avoids repetition
- **Interactive UI**: Clean, user-friendly Streamlit interface
- **Score Tracking**: Comprehensive scoring system with percentage calculation
- **Celebration Effects**: Balloon animations for excellent performance (≥80%)

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Framework**: Langchain
- **Language Model**: Google Gemini 1.5 Flash
- **Backend**: Python
- **Parsing**: Custom regex-based parser
- **State Management**: Streamlit session state

## 📋 Prerequisites

- Python 3.8 or higher
- Google AI API Key (Gemini)
- Internet connection for API calls

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jainish21705/Quiz-Generator-using-Langchain-and-Gemini.git
   cd Quiz-Generator-using-Langchain-and-Gemini
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

4. **Get your Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file

## 🚀 Usage

1. **Run the application**
   ```bash
   streamlit run quiz_app.py
   ```

2. **Generate a Quiz**
   - Enter your topic/context in the text area
   - Select difficulty level (Easy, Medium, Hard)
   - Choose number of questions (1-5)
   - Click "Generate Quiz"

3. **Take the Quiz**
   - Answer each multiple-choice question
   - Get instant feedback on your selections
   - Submit to see your final score

4. **View Results**
   - See detailed scoring with percentage
   - Review correct answers for incorrect responses
   - Enjoy celebration effects for high scores!

## 📁 Project Structure

```
├── quiz_app.py          # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
└── README.md           # Project documentation
```

## 🔍 Key Components

### QuizParser Class
Custom output parser that extracts structured quiz data from AI responses using regex patterns:
- Parses questions with numbered tags
- Extracts multiple-choice options
- Matches correct answers to questions

### Quiz Generation Chain
Langchain pipeline that combines:
- **PromptTemplate**: Structured prompt for consistent quiz format
- **Gemini LLM**: Google's language model for content generation
- **Custom Parser**: Processes AI output into usable quiz format

### State Management
Streamlit session state handles:
- Quiz data persistence
- User answer tracking
- Score calculation
- Generation history for uniqueness

## 🎯 Features in Detail

### Intelligent Question Generation
- **Uniqueness Tracking**: Prevents duplicate questions across generations
- **Context-Aware**: Generates questions specific to your input topic
- **Difficulty Scaling**: Adjusts question complexity based on selected level
- **Format Consistency**: Ensures proper multiple-choice structure

### Interactive Feedback System
- **Real-time Validation**: Immediate feedback on answer selection
- **Color-coded Responses**: Green for correct, red for incorrect
- **Correct Answer Display**: Shows the right answer for wrong selections
- **Progress Tracking**: Visual progress indicator

### Scoring System
- **Percentage Calculation**: Shows score as both fraction and percentage
- **Performance Categories**: 
  - Excellent (≥80%): Balloon celebration + success message
  - Good (≥60%): Encouraging success message
  - Needs Improvement (<60%): Motivational message

## 🔒 Security & Best Practices

- Environment variables for API key management
- Error handling for API failures
- Input validation for user inputs
- Session state management for data persistence

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `.env` file exists with correct `GEMINI_API_KEY`
   - Verify API key is valid and has sufficient quota

2. **Quiz Generation Fails**
   - Check internet connection
   - Try with simpler topic context
   - Reduce number of questions

3. **Parsing Errors**
   - Usually resolved by regenerating the quiz
   - Check if topic context is clear and specific

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Google AI** for the Gemini language model
- **Langchain** for the excellent AI framework
- **Streamlit** for the intuitive web app framework
- **OpenAI** for inspiring AI-powered educational tools

## 📊 Future Enhancements

- [ ] Support for True/False questions
- [ ] Export quiz results to PDF
- [ ] Database integration for quiz history
- [ ] Multi-language support
- [ ] Bulk question generation
- [ ] Advanced analytics dashboard
- [ ] Question difficulty analysis
- [ ] Timer functionality for timed quizzes

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Contact the maintainer

---

⭐ If you found this project helpful, please give it a star on GitHub!
