import * as Color from 'color-js';
import { Sentiments } from 'src/tweet/tweet-card';

export enum AppColorPalette {
    SENTIMENT_GREEN = '#61D800',
    SENTIMENT_RED = '#D32F2F',
    SENTIMENT_BLUE = '#2196F3',
    APP_BLUE = '#30CDFF',
    APP_WHITE = '#FFFFFF'
}

export class ColourUtil {
    public static getColourForSentimentAndAttention(sentiment: Sentiments, attention: number): string {
        let color: Color;
        switch (sentiment) {
            case Sentiments.POSITIVE:
                color = Color(AppColorPalette.SENTIMENT_GREEN);
                break;
            case Sentiments.NEUTRAL:
                color = Color(AppColorPalette.SENTIMENT_BLUE);
                break;
            case Sentiments.NEGATIVE:
                color = Color(AppColorPalette.SENTIMENT_RED);
                break;
            default:
                color = Color(AppColorPalette.APP_WHITE);
                break;
        }


        const truncatedAttention: number = !!attention ? +attention.toPrecision(2) : 0;

        const alphaColor: Color = color.setAlpha(truncatedAttention);

        return alphaColor.toCSS();
    }
}