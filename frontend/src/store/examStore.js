import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useExamStore = create(
  persist(
    (set, get) => ({
      currentTest: null,
      questions: [],
      answers: {},
      currentQuestionIndex: 0,
      markedForReview: [],
      timeRemaining: 0,
      isSubmitted: false,
      isLoading: false,
      examName: '',

      setTest: (test, questions) => {
        // Determine duration in minutes from several possible fields
        const durationMinutes = (
          test?.duration ??
          test?.duration_minutes ??
          test?.exam?.duration_minutes ??
          test?.exam?.duration ??
          null
        );
        const computedMinutes = Number(durationMinutes) || Math.max(1, Math.ceil((test?.total_questions || questions.length || 20) / 2));
        const durationSeconds = computedMinutes * 60;

        set({
          currentTest: { ...test, duration_seconds: durationSeconds, duration_minutes: computedMinutes },
          questions: questions,
          answers: {},
          currentQuestionIndex: 0,
          markedForReview: [],
          timeRemaining: durationSeconds,
          isSubmitted: false,
          examName: test.name || 'Mock Test'
        });
      },

      setAnswer: (questionId, answer) => {
        set((state) => ({
          answers: { ...state.answers, [questionId]: answer }
        }));
      },

      clearAnswer: (questionId) => {
        set((state) => {
          const newAnswers = { ...state.answers };
          delete newAnswers[questionId];
          return { answers: newAnswers };
        });
      },

      toggleMarkForReview: (questionId) => {
        set((state) => {
          const isMarked = state.markedForReview.includes(questionId);
          if (isMarked) {
            return { markedForReview: state.markedForReview.filter(id => id !== questionId) };
          } else {
            return { markedForReview: [...state.markedForReview, questionId] };
          }
        });
      },

      nextQuestion: () => {
        set((state) => {
          if (state.currentQuestionIndex < state.questions.length - 1) {
            return { currentQuestionIndex: state.currentQuestionIndex + 1 };
          }
          return state;
        });
      },

      prevQuestion: () => {
        set((state) => {
          if (state.currentQuestionIndex > 0) {
            return { currentQuestionIndex: state.currentQuestionIndex - 1 };
          }
          return state;
        });
      },

      goToQuestion: (index) => {
        set({ currentQuestionIndex: index });
      },

      tick: () => {
        set((state) => {
          if (state.timeRemaining > 0 && !state.isSubmitted) {
            return { timeRemaining: state.timeRemaining - 1 };
          } else if (state.timeRemaining === 0 && !state.isSubmitted) {
             return { isSubmitted: true }; // Auto submit on 0
          }
          return state;
        });
      },

      resetExam: () => {
        set({
          currentTest: null,
          questions: [],
          answers: {},
          currentQuestionIndex: 0,
          markedForReview: [],
          timeRemaining: 0,
          isSubmitted: false,
          examName: ''
        });
      },
      
      setLoading: (bool) => set({ isLoading: bool }),
    }),
    {
      name: 'mockbees-exam',
      partialize: (state) => ({
        currentTest: state.currentTest,
        questions: state.questions,
        answers: state.answers,
        currentQuestionIndex: state.currentQuestionIndex,
        markedForReview: state.markedForReview,
        timeRemaining: state.timeRemaining,
        isSubmitted: state.isSubmitted,
        examName: state.examName
      })
    }
  )
);

export default useExamStore;
