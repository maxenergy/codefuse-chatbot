# encoding: utf-8
'''
@author: 温进
@file: code_analyzer.py
@time: 2023/11/21 下午2:27
@desc:
'''
import time
from loguru import logger

from coagent.codechat.code_analyzer.code_static_analysis import CodeStaticAnalysis
from coagent.codechat.code_analyzer.code_intepreter import CodeIntepreter
from coagent.codechat.code_analyzer.code_preprocess import CodePreprocessor
from coagent.codechat.code_analyzer.code_dedup import CodeDedup
from coagent.llm_models.llm_config import LLMConfig



class CodeAnalyzer:
    def __init__(self, language: str, llm_config: LLMConfig):
        self.llm_config = llm_config
        self.code_preprocessor = CodePreprocessor()
        self.code_debup = CodeDedup()
        self.code_interperter = CodeIntepreter(self.llm_config)
        self.code_static_analyzer = CodeStaticAnalysis(language=language)

    def analyze(self, code_dict: dict, do_interpret: bool = True):
        '''
        analyze code
        @param code_dict: {fp: code_text}
        @param do_interpret: Whether to get analysis result
        @return:
        '''
        # preprocess and dedup
        st = time.time()
        code_dict = self.code_preprocessor.preprocess(code_dict)
        code_dict = self.code_debup.dedup(code_dict)
        logger.debug('preprocess and dedup rt={}'.format(time.time() - st))

        # static analysis
        st = time.time()
        static_analysis_res = self.code_static_analyzer.analyze(code_dict)
        logger.debug('static analysis rt={}'.format(time.time() - st))

        # interpretation
        if do_interpret:
            logger.info('start interpret code')
            st = time.time()
            code_list = list(code_dict.values())
            interpretation = self.code_interperter.get_intepretation_batch(code_list)
            logger.debug('interpret rt={}'.format(time.time() - st))
        else:
            interpretation = {i: '' for i in code_dict.values()}

        return static_analysis_res, interpretation


if __name__ == '__main__':
    engine = 'openai'
    language = 'java'
    code_dict = {'1': '''package com.theokanning.openai.client;
import com.theokanning.openai.DeleteResult;
import com.theokanning.openai.OpenAiResponse;
import com.theokanning.openai.audio.TranscriptionResult;
import com.theokanning.openai.audio.TranslationResult;
import com.theokanning.openai.billing.BillingUsage;
import com.theokanning.openai.billing.Subscription;
import com.theokanning.openai.completion.CompletionRequest;
import com.theokanning.openai.completion.CompletionResult;
import com.theokanning.openai.completion.chat.ChatCompletionRequest;
import com.theokanning.openai.completion.chat.ChatCompletionResult;
import com.theokanning.openai.edit.EditRequest;
import com.theokanning.openai.edit.EditResult;
import com.theokanning.openai.embedding.EmbeddingRequest;
import com.theokanning.openai.embedding.EmbeddingResult;
import com.theokanning.openai.engine.Engine;
import com.theokanning.openai.file.File;
import com.theokanning.openai.fine_tuning.FineTuningEvent;
import com.theokanning.openai.fine_tuning.FineTuningJob;
import com.theokanning.openai.fine_tuning.FineTuningJobRequest;
import com.theokanning.openai.finetune.FineTuneEvent;
import com.theokanning.openai.finetune.FineTuneRequest;
import com.theokanning.openai.finetune.FineTuneResult;
import com.theokanning.openai.image.CreateImageRequest;
import com.theokanning.openai.image.ImageResult;
import com.theokanning.openai.model.Model;
import com.theokanning.openai.moderation.ModerationRequest;
import com.theokanning.openai.moderation.ModerationResult;
import io.reactivex.Single;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.*;
import java.time.LocalDate;
public interface OpenAiApi {
    @GET("v1/models")
    Single<OpenAiResponse<Model>> listModels();
    @GET("/v1/models/{model_id}")
    Single<Model> getModel(@Path("model_id") String modelId);
    @POST("/v1/completions")
    Single<CompletionResult> createCompletion(@Body CompletionRequest request);
    @Streaming
    @POST("/v1/completions")
    Call<ResponseBody> createCompletionStream(@Body CompletionRequest request);
    @POST("/v1/chat/completions")
    Single<ChatCompletionResult> createChatCompletion(@Body ChatCompletionRequest request);
    @Streaming
    @POST("/v1/chat/completions")
    Call<ResponseBody> createChatCompletionStream(@Body ChatCompletionRequest request);
    @Deprecated
    @POST("/v1/engines/{engine_id}/completions")
    Single<CompletionResult> createCompletion(@Path("engine_id") String engineId, @Body CompletionRequest request);
    @POST("/v1/edits")
    Single<EditResult> createEdit(@Body EditRequest request);
    @Deprecated
    @POST("/v1/engines/{engine_id}/edits")
    Single<EditResult> createEdit(@Path("engine_id") String engineId, @Body EditRequest request);
    @POST("/v1/embeddings")
    Single<EmbeddingResult> createEmbeddings(@Body EmbeddingRequest request);
    @Deprecated
    @POST("/v1/engines/{engine_id}/embeddings")
    Single<EmbeddingResult> createEmbeddings(@Path("engine_id") String engineId, @Body EmbeddingRequest request);
    @GET("/v1/files")
    Single<OpenAiResponse<File>> listFiles();
    @Multipart
    @POST("/v1/files")
    Single<File> uploadFile(@Part("purpose") RequestBody purpose, @Part MultipartBody.Part file);
    @DELETE("/v1/files/{file_id}")
    Single<DeleteResult> deleteFile(@Path("file_id") String fileId);
    @GET("/v1/files/{file_id}")
    Single<File> retrieveFile(@Path("file_id") String fileId);
    @Streaming
    @GET("/v1/files/{file_id}/content")
    Single<ResponseBody> retrieveFileContent(@Path("file_id") String fileId);
    @POST("/v1/fine_tuning/jobs")
    Single<FineTuningJob> createFineTuningJob(@Body FineTuningJobRequest request);
    @GET("/v1/fine_tuning/jobs")
    Single<OpenAiResponse<FineTuningJob>> listFineTuningJobs();
    @GET("/v1/fine_tuning/jobs/{fine_tuning_job_id}")
    Single<FineTuningJob> retrieveFineTuningJob(@Path("fine_tuning_job_id") String fineTuningJobId);
    @POST("/v1/fine_tuning/jobs/{fine_tuning_job_id}/cancel")
    Single<FineTuningJob> cancelFineTuningJob(@Path("fine_tuning_job_id") String fineTuningJobId);
    @GET("/v1/fine_tuning/jobs/{fine_tuning_job_id}/events")
    Single<OpenAiResponse<FineTuningEvent>> listFineTuningJobEvents(@Path("fine_tuning_job_id") String fineTuningJobId);
    @Deprecated
    @POST("/v1/fine-tunes")
    Single<FineTuneResult> createFineTune(@Body FineTuneRequest request);
    @POST("/v1/completions")
    Single<CompletionResult> createFineTuneCompletion(@Body CompletionRequest request);
    @Deprecated
    @GET("/v1/fine-tunes")
    Single<OpenAiResponse<FineTuneResult>> listFineTunes();
    @Deprecated
    @GET("/v1/fine-tunes/{fine_tune_id}")
    Single<FineTuneResult> retrieveFineTune(@Path("fine_tune_id") String fineTuneId);
    @Deprecated
    @POST("/v1/fine-tunes/{fine_tune_id}/cancel")
    Single<FineTuneResult> cancelFineTune(@Path("fine_tune_id") String fineTuneId);
    @Deprecated
    @GET("/v1/fine-tunes/{fine_tune_id}/events")
    Single<OpenAiResponse<FineTuneEvent>> listFineTuneEvents(@Path("fine_tune_id") String fineTuneId);
    @DELETE("/v1/models/{fine_tune_id}")
    Single<DeleteResult> deleteFineTune(@Path("fine_tune_id") String fineTuneId);
    @POST("/v1/images/generations")
    Single<ImageResult> createImage(@Body CreateImageRequest request);
    @POST("/v1/images/edits")
    Single<ImageResult> createImageEdit(@Body RequestBody requestBody);
    @POST("/v1/images/variations")
    Single<ImageResult> createImageVariation(@Body RequestBody requestBody);
    @POST("/v1/audio/transcriptions")
    Single<TranscriptionResult> createTranscription(@Body RequestBody requestBody);
    @POST("/v1/audio/translations")
    Single<TranslationResult> createTranslation(@Body RequestBody requestBody);
    @POST("/v1/moderations")
    Single<ModerationResult> createModeration(@Body ModerationRequest request);
    @Deprecated
    @GET("v1/engines")
    Single<OpenAiResponse<Engine>> getEngines();
    @Deprecated
    @GET("/v1/engines/{engine_id}")
    Single<Engine> getEngine(@Path("engine_id") String engineId);
    /**
     * Account information inquiry: It contains total amount (in US dollars) and other information.
     *
     * @return
     */
    @Deprecated
    @GET("v1/dashboard/billing/subscription")
    Single<Subscription> subscription();
    /**
     * Account call interface consumption amount inquiry.
     * totalUsage = Total amount used by the account (in US cents).
     *
     * @param starDate
     * @param endDate
     * @return Consumption amount information.
     */
    @Deprecated
    @GET("v1/dashboard/billing/usage")
    Single<BillingUsage> billingUsage(@Query("start_date") LocalDate starDate, @Query("end_date") LocalDate endDate);
}''', '2': '''
package com.theokanning.openai;

/**
 * OkHttp Interceptor that adds an authorization token header
 * 
 * @deprecated Use {@link com.theokanning.openai.client.AuthenticationInterceptor}
 */
@Deprecated
public class AuthenticationInterceptor extends com.theokanning.openai.client.AuthenticationInterceptor {

    AuthenticationInterceptor(String token) {
        super(token);
    }

}
'''}

    ca = CodeAnalyzer(engine, language)
    res = ca.analyze(code_dict)
    logger.debug(res)
